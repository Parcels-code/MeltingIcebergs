'''
Code for modern Antarctic iceberg simulations
---------------------------------------------
#(!)#  marks changes required every run (filename, files)
'''

#================================== IMPORT ===================================#
import parcels
from glob import glob
import hashlib
import json
import time
from pathlib import Path

import numpy as np
import xarray as xr
import copernicusmarine

import sys
sys.path.append('{path_to_main_folder}/MeltingIcebergs_v4/input_files')


#==================== LOAD/SELECT DATA & DEFINE FIELDSET ====================#

DATASET_IDs_BY_GRID = [
    (
        "physics_mon",
        [
            ("cmems_mod_glo_phy_my_0.083deg_P1D-m", ("uo", "vo", "thetao")),
        ],
    ),
    (
        "wind_mon",
        [
            (
                "cmems_obs-wind_glo_phy_my_l4_0.125deg_PT1H",
                ("northward_stress", "eastward_stress"),
            ),
        ],
    ),
    (
        "bathy_mon",
        [
            ("cmems_mod_glo_phy_anfc_0.083deg_static", ("deptho",)),
        ],
    ),
]

spatial_kwargs = {
    "minimum_latitude": -70,
    "maximum_latitude": -30,
    "minimum_longitude": -80,
    "maximum_longitude": 50,
}

time_kwargs = {
    "start_datetime": "2024-01-01",
    "end_datetime": "2024-01-31",
}

output_dir = Path(
    "/{path_to_main_folder}/MeltingIcebergs_v4/input_files"
)
output_dir.mkdir(parents=True, exist_ok=True)

datasets = {}
fset = []

for name, grid_datasets in DATASET_IDs_BY_GRID:
    print(f"Downloading {name}...")

    open_kwargs = dict(spatial_kwargs)
    if name != "bathy":
        open_kwargs.update(time_kwargs)

    downloaded = [
        copernicusmarine.open_dataset(
            dataset_id,
            variables=list(used_vars),
            **open_kwargs,
        )
        for dataset_id, used_vars in grid_datasets
    ]

    ds = xr.merge(downloaded) if len(downloaded) > 1 else downloaded[0]

    # Save a copy to disk
    output_file = output_dir / f"{name}.nc"
    ds.to_netcdf(output_file)

    print(f"Saved {name} to {output_file}")