# MeltingIcebergs_v4
❗ Note: This is the official code repository for MeltingIcebergs in Parcels version 4

## :page_with_curl: Description
This repository contains the code used to perform depth-integrated Lagrangian iceberg tracing around Antarctica during modern conditions. Using the Parcels framework, iceberg melting (or growth) is simulated using several kernels, including for the dominant iceberg melt terms: basal melt, buoyant convection and wave erosion. By defining kernels for five different order-of-magnitude iceberg size classes, the model can be used to track iceberg melt trajectories. 

## ⚙️ Dependencies
The model was run using Python 3.8.13.

The files have the following dependencies:
* cartopy (0.25.0)
* cmocean (3.2.1)
* matplotlib-inline (0.2.2)
* pandas (3.0.6)
* parcels (4.0.0)
* shapely (2.1.2)

### Environment file
To set up an environment with the dependencies directly, one could use the 'meltingicebergs.yml' file using:
```
conda env create -f MeltingIcebergs_v4.yml
conda activate MeltingIcebergs_v4
```

## :file_folder: Folder Structure
1) preparation_files: Model files used to prepare the simulations.
2) analysis_files: Analyse specific model components.
3) plotting_files: Notebooks used to generate plots and animations.
4) iceberg_simulations: Model code to simulate iceberg trajectories.
5) iceberg_model: Model code (kernels) to initialise and adapt the icebergs throughout the simulation.

```bash
|   CITATION.cff
│   MeltingIcebergs_v4.yml
│   code_dev_v4.ipynb
│   README.md
│
│
├───iceberg_simulations
│       modern_icebergs_integrated.py
│
├───iceberg_model
│       icebergs_kernels.py
│       icebergs_particleclass.py
│
├───plotting_files
│       PaperFigures-Modern.ipynb
│
└───preparation_files
        download_copernicus_dataset.py
```

## :computer: Code Usage
All simulations require the files in the 'iceberg_model' folder to define the kernels and iceberg particle class used in the model. By adapting these files, one could, for example, define new iceberg-size classes, implement different melt parameterisations, or change the stored model variables. Some of the variables used here (salinity, Monin-Obukof length) were determined outside of the model in the files from the 'analysis_files' folder.

Using the files in the 'preparation_files' folder require enough desk space (±300 GB). One could download less data to decrease this amount.

For a short modern simulation, the 'modern_icebergs_integrated.py' file in the 'iceberg_simulations' folder is needed. These simulations use CopernicusMarine for ocean temperature and velocity components, the surface wind components, and bathymetry. These simulations cover only the year 2024.

To recreate the figures and animations shown in the paper and supplements, one can use the notebooks in the 'plotting_files' folder.

## :envelope_with_arrow: Contact and contribution
For questions about this repository, please contact the authors, [Fleur Rothstegge](https://github.com/fleurrothstegge) (f.l.p.rothstegge@uu.nl) or [Erik van Sebille](https://github.com/erikvansebille) (e.vansebille@uu.nl), or open an Issue or Pull request in this repository.

## :balance_scale: License
This repository is licensed under an MIT License. You can view the [LICENSE here](https://github.com/OceanParcels/MeltingIcebergs/blob/main/LICENSE)

## :bookmark: Cite this repository
This repository can be found at: <a href="https://zenodo.org/doi/10.5281/zenodo.11208937"><img src="https://zenodo.org/badge/693549425.svg" alt="DOI"></a>.


