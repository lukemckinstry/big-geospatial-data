# GUS 8061 - Big Geospatial Data

**Lee Hachadoorian**\
**Spring 2023**

Based on materials created by Xiaojiang Li, PhD, Department of Geography and Urban Studies, Temple University, <http://www.urbanspatial.info/>. Forked from Prof. Li's Spring 2022 course repo at <https://github.com/xiaojianggis/big-spatial-data/>.

**UNDER CONSTRUCTION:** Some of the materials are being altered. Numbering generally corresponds to course weeks. Associated assignments appear in Canvas. See my notes regarding the state of each notebook, as well as notes below regarding preparing your environment, obtaining data, and what changes I am making and why.

Most of the materials in this repo are Jupyter Notebooks. You can create a Python environment in any way you wish, but instructions are provided below for creating a conda environment using the YAML environment file included in this repo.

## 1. Configure Environment and Python basics

1. [Install Anaconda and configure Python module](lab1-basics-python-spatial-programing/install-anaconda.md)
2. [Become familar with Jupyter Notebook](lab1-basics-python-spatial-programing/jupyter-notebook.md)
3. [Python basics](01_basics_python_spatial_data.ipynb))

## 2. Basics of GIS programming

These notebooks are short and will be combined into one longer notebook.

1. [Python spatial module ecosystem](02-1_read_shapefile_gdal.ipynb)
2. [Using Geopandas to read shapefiles and do spatial join](02-3_geopandas_spatial_analysis.ipynb)

## 3. Spatial Data Manipulation

The exercise [Using Fiona to manipulate shapefiles and do spatial analysis](03_spatial_analysis_fiona_shapely.ipynb) has the following sections:

1. Read Shapefile using Fiona
2. Using Fiona and Shapely to overlay shapefiles

## 4. Raster data operations

**Currently nonworking. Need to obtain certificate file for NAIP download.**

1. [Download NAIP images automatically](04_naip_downloader.ipynb)
2. [Using Rasterio to manipulate geo-reference raster data](04_raster_data_manipulation.ipynb)
    * Mosaic, mask, clip
    * Calculate NDVI
    * Overlay vector data on raster (zonal statistics)]

## 5. Spatial database

1. Install Postgres/PostGIS
2. SQL Basics
3. Spatial Analyses through SQL queries

## 6. Access Spatial Database using Python ([link](lab6-access-db-python/querydb_python.ipynb))

1. Access Postgres/PostGIS database using Python
2. Read shapefile and save features into database tables using Python
3. Save query results into shapefiles using Python

## 7. AWS (On canvas)

## 8. Google Earth Engine (On canvas)

## 9. Big data visualization

[Visualizing half-million building blocks online](09_buildingblock_viz.md)

This exercise covers the following steps:

1. Convert shapefile to geojson and mbtile
2. Using Mapbox studio to visualize building blocks
3. Using GitHub to host your web map

# Preparing Your Python Environment

**TL;DR** Download [geospatial-environment.yml](geospatial-environment.yml) (or just clone this repo). Open the Anaconda Prompt. Navigate to the directory with the environment file and run the following conda command:

```
conda env create -f geospatial-environment.yml
```

This will create a conda environment named `geospatial` with *almost* all of the packages you will need for the entire semester.

## The Longer Version

You can create your Python environment in whatever way you are comfortable. I prefer using Anaconda, and that is what I will show in this class. If you prefer to work with Python environments using pip or some other way, this is the list of packages that you need:

- geopandas
- rasterio
- descartes
- jupyter
- matplotlib
- sqlalchemy
- psycopg2
- boto3
- smart_open
- scikit-learn-intelex
- progressbar2
- tqdm
- pysolar

If you use pip, all of these packages are available in PyPI.

If you use Anaconda, I have set `python=3.8` to avoid unsatisfiable package conflicts. All of these packages are available in the default conda channel *except* pysolar. The conda environment file has the line `- conda-forge::pysolar` commented out. You can experiment with uncommenting it, but I have found that attempting to install it at environment creation takes an inordinately long time and often fails. Without it, environment creation runs pretty quickly (2-3 minutes). You can install pysolar afterward, and this works consistently (and quickly), even if Anaconda can't figure out how to do it in one go. Resorting to pip for pysolar or any other package seems unnecessary, so long as you are working with Python 3.8. You can install pysolar by activating the new `geospatial` environment and calling `conda install`:

```
conda install -c conda-forge pysolar
```

Additionally, I have included Spyder (my preferred IDE) and PyQtWebEngine (necessary for Spyder to run, but for some reason not a dependency). If you will stick to the Jupyter Notebooks or prefer another IDE, you can remove or comment out the following lines in the environment file before creating the environment:

```
  - spyder
  - pyqtwebengine
```

# Acquiring the Notebooks and Data

You can download individual notebooks and data files as needed.

The easiest way to acquire the notebooks and data is to clone this repository:

```
https://github.com/leehach/big-geospatial-data.git
```

If you don't have Git installed, you can instead [download the repo as a ZIP](https://github.com/leehach/big-geospatial-data/archive/refs/heads/main.zip). Of course, if there are changes, you will have to redownload changed files or the entire repo, whereas if you clone the repo you can update the files with `git pull`.

Some notebooks require downloading data (usually large files or data available via API) from other sources.

The repo contains an untracked `output` directory. When you create this repo, you should create `output` as a subdirectory of your main working directory. The notebooks will direct all created data to this repo. In some instances, large file downloads may also be expected to be *read* from `output`. This somewhat violates the nomenclature, but allows us to maintain one untracked directory for files that we don't want to accidentally end up in the remote.

