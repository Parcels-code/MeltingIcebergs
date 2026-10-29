'''
Code for modern Antarctic iceberg simulations
---------------------------------------------
#(!)#  marks changes required every run (filename, files)
'''

#================================== IMPORT ===================================#
import parcels
import time
from pathlib import Path

import numpy as np
import xarray as xr

import sys
sys.path.append('{path_to_main_folder}/MeltingIcebergs_v4/iceberg_model')

import icebergs_kernels_v4 as kernels
import icebergs_particleclass_v4 as particleclass


def report_rss(label):
    for line in Path("/proc/self/status").read_text().splitlines():
        if line.startswith("VmRSS:"):
            rss_gib = int(line.split()[1]) / 1024**2
            print(f"{label}: RSS={rss_gib:.2f} GiB", flush=True)
            return


#==================== LOAD/SELECT DATA & DEFINE FIELDSET ====================#

data_dir = Path(
    "{path_to_main_folder}/MeltingIcebergs_v4/input_files"
)

chunk_sizes = {
    "physics": {"time": 1, "depth": 10, "latitude": 128, "longitude": 256},
    "wind": {"time": 24, "latitude": 128, "longitude": 256},
    "bathy": {"latitude": 128, "longitude": 256},
}

datasets_raw = {
    name: xr.open_dataset(data_dir / f"{name}.nc", chunks=chunk_sizes[name])
    for name in chunk_sizes
}

datasets = {}
fset = []

for name, ds in datasets_raw.items():

    if name in ("physics", "wind"):
        time_dim = next(
            (dim for dim in ("time", "time_counter") if dim in ds.dims),
            None,
        )
        if time_dim is None:
            raise ValueError(
                f"No time dimension found in {name}: {dict(ds.sizes)}"
            )

        # ds = ds.sel(
        #     {time_dim: slice("2024-01-01", "2024-01-31T23:59:59")}
        # )

    if name == "bathy":
        if "deptho" not in ds.data_vars:
            raise ValueError(
                "The bathymetry dataset does not contain 'deptho'."
            )
        print("Bathymetry dimensions:", ds["deptho"].dims)
        print("Bathymetry attributes:", ds["deptho"].attrs)

    if "uo" in ds.data_vars and "vo" in ds.data_vars:
        ds = ds.rename({"uo": "U", "vo": "V"})
        vector_fields = {"UV": ("U", "V")}

    elif (
        "northward_stress" in ds.data_vars
        and "eastward_stress" in ds.data_vars
    ):
        vector_fields = {
            "XY": ("northward_stress", "eastward_stress")
        }

    else:
        vector_fields = {}


    report_rss(f"{name}: before S-grid conversion")
    datasets[name] = parcels.convert.copernicusmarine_to_sgrid(
        fields={
            var_name: da
            for var_name, da in ds.data_vars.items()
        }
    )

    for var_name, da in datasets[name].data_vars.items():
        print(
            f"{name}.{var_name}: "
            f"dask={hasattr(da.data, '__dask_graph__')}, chunks={da.chunks}",
            flush=True,
        )
    report_rss(f"{name}: after S-grid conversion")

    fset.append(
        parcels.FieldSet.from_sgrid_conventions(
            datasets[name],
            vector_fields=vector_fields,
        )
    )

    report_rss(f"{name}: after FieldSet construction")
    print(f"Done with {name}", flush=True)

fieldset = fset[0]
for fieldset_part in fset[1:]:
    fieldset += fieldset_part

fieldset.to_windowed_arrays()
# # fieldset.to_chunk_cached_arrays()

fieldset.describe()
#==================== DEFINE PARTICLESET ====================#
### Define particle class
pclass = particleclass.Iceberg_FW

### Define start locations
# Forwards
# 25 start locations based on Starr et al., 2021

lons = np.array([-49.4878, -44.4064, -51.9983, -45.7632, -52.1467,
                    -46.6411, -49.2031, -52.701, -50.6276, -47.6291,
                    -50.6072, -48.3745, -50.6544, -50.2465, -49.3528, 
                    -48.937, -50.1882, -50.3123, -47.5602, -49.0983,
                    -50.5165, -52.5448, -50.6169, -50.5114, -48.5969, 
                    -50.193, -50.7368, -50.7244, -52.2803])
lats = np.array([-64.3257, -62.8802, -63.296, -63.8265, -63.2629,
                    -64.298, -64.6458, -64.4646, -64.7549, -64.8559,
                    -68.7443, -64.6387, -69.8753, -66.9758, -65.4979,
                    -64.6637, -66.958, -67.0103, -65.4742, -64.6985,
                    -68.8178, -64.4642, -68.7282, -68.7956, -65.2012,
                    -65.9453, -63.6841, -63.7504, -64.0858])


### Define global parameters
fieldset.add_context('ODP_lat', -61.849083)  # Latitude ODP 696 present-day [°]
fieldset.add_context('ODP_lon', -42.933067)  # Longitude ODP 696 present-day [°]
fieldset.add_context('rho_i', 850.0)         # Ice density [kg/m3]
fieldset.add_context('rho_o', 1027.5)        # Ocean density [kg/m3]
fieldset.add_context('rho_a', 1.293)         # Air density [kg/m3]
fieldset.add_context('Ti', -1.92)            # Freezing temperature [°C] --> average determined from salinity field 00380101 in Weddell Sea
fieldset.add_context('sec_to_day', 86400.)   # Seconds per day [s/d]

def TimedSampleFields(particles, fieldset):
    started = time.perf_counter()
    try:
        kernels.SampleFields(particles, fieldset)
    finally:
        print(
            f"SampleFields at t={particles.t[0]}: {time.perf_counter() - started:.2f} s",
            flush=True,
        )


### Load particleset
pset = parcels.ParticleSet(fieldset, 
                           pclass = pclass,
                           x = lons,
                           y = lats,
                           z = np.full(len(lats), [0]))

kernels_FW = [
    kernels.SetInitialPropertiesC4,
    kernels.NewProperties,
    kernels.SampleFields,
    kernels.BuoyantConvection,
    kernels.BasalMelt,
    kernels.WaveErosion,
    kernels.Grounding,
    parcels.kernels.AdvectionRK2,
]

kernels_surface = [
    kernels.SetInitialPropertiesC4,
    kernels.NewProperties,
    kernels.SampleFieldsSurf,
    kernels.BuoyantConvectionSurf,
    kernels.BasalMeltSurf,
    kernels.WaveErosionSurf,
    parcels.kernels.AdvectionRK2
]

#==================== EXECUTE ====================#
### Define output file #(!)#
oufile = parcels.ParticleFile(
    "{path_to_main_folder}/output_files/output_testing_chunk_363D.parquet", 
    outputdt = np.timedelta64(1, "D"), 
        mode ="w",
        )
                              
### Execute #(!)#
## Daily
pset.execute(
    kernels_FW, 
    dt=np.timedelta64(1, 'h'),
    runtime=np.timedelta64(363, "D"),
    output_file = oufile,
)


oufile.close()