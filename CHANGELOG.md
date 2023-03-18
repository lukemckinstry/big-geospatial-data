# CHANGELOG

2023 Spring\
Lee Hachadoorian\
Lee.Hachadoorian@temple.edu

Repo forked from Prof. Xiaojiang Li's original course repo at <https://github.com/xiaojianggis/big-spatial-data> in Spring 2023. This log contains a history of notable changes made over the course of the semester.

## Repository Changes

* File hierarchy flattened---all Jupyter notebooks or instructional guides moved to root folder.
* All input data moved to /data folder. No exercise-specific data subfolders.
* All output directed to /output folder which is excluded from repo via .gitignore.
* Some input data is too large to host in repo, and students must download directly. All scripts have been modified to find such files in the /output folder so that it is excluded from repo.
* All shapefiles converted to GeoPackages using [convert_shp_to_gpkg.py](convert_shp_to_gpkg.py).
* All .DS_Store files removed
* .ipynb_checkpoints added to gitignore

## Lab Exercise Changes

1. Environment YML file provided for creation of `geospatial` conda environment with all packages necessary for the semester.
    
    > Note that conda environment includes boto3 and smart_open, before I figured out that these are never used locally. They are only ever used in an AWS instance.
2. Removed `!pip install` statements from all lab exercises.
3. Formatted strings replaced with f-strings throughout. (Any that have not been replaced are oversights.)

### 1, 2, 3

Largely the same except for minor edits and additional explanation.

### 4. Raster Data Operations

This exercise needs to be fixed or replaced. Microsoft Planetary Computer changed API and I was unable to get the data downloader to work with the new API. I manually downloaded NAIP imagery, but was uanble to obtain the NIR (near infrared) imagery necessary for NDVI calculations.

### 5. Intro PostGIS

1. Instructions converted to Markdown (PDF deleted).
2. PostGIS installed as Docker container rather than using EnterpriseDB native installer.
3. GUI-based file upload via QGIS instead of shp2pgsql-gui.
4. CLI-based file upload via ogr2ogr instead of shp2pgsql.

### 6. Access Spatial Database Using Python

Largely the same. Connection parameters updated to point to Docker PostGIS container.

This lab exercise is not terribly complex and can probably be combined with Lab 5 (which has no assignment to submit anyway). I think they can both be covered in a single class session if the students are assigned the installation of Docker and PostGIS as class prep for Lab 5.

### 7. AWS

1. Instructions created in Markdown from lecture slides and previously recorded video.
2. S3 access provided by IAM role attached to EC2 instance. No longer need to install AWS CLI or use `aws configure` to set up S3 access.
3. File upload/download via WinSCP instead of `scp` at the command line.

Recommend requiring students to create AWS account and set up EC2 instance and S3 buckets prior to class. Connecting to Jupyter notebook server running in EC2 is a little more complex and can be demoed in class.

### 8. Google Earth Engine

Forthcoming.
