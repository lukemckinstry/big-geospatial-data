# CHANGELOG

2023 Spring\
Lee Hachadoorian\
Lee.Hachadoorian@temple.edu

Repo forked from Prof. Xiaojiang Li's original course repo at <https://github.com/xiaojianggis/big-spatial-data> in Spring 2023. This log contains a history of notable changes made over the course of the semester.

## Repository Changes

* File hierarchy flattened---all Jupyter notebooks or instructional guides moved to root folder.
    * Exception is Lab 1. The lab1-basics-python-spatial-programming folder with setup instructions for Anaconda and Jupyter notebook has been renamed setup. The Lab 1 notebook has been moved to the root folder.
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
4. Remote Jupyter notebook port forwarding changes from `8888:localhost:8157` to `8157:localhost:8888`. I think the intended purpose of using port forwarding is to avoid claiming the *local* `8888` port so the student can simultaneously connect to the remote Jupyter server while also running a local Jupyter server on the default port. There is no conflict for port `8888` on the *remote* server, so starting the remote server on a different port doesn't seem terribly useful.
5. Slideshow Lab5-Geog 573 Cloud Computing- Spring2020.pdf removed. This was from an outside course and largely redundant with material in this lab. The only new part was a few slides on using Hive and Hadoop to run Postgres queries in AWS. If that topic will be introduced, it should be integrated into the main lab.

Recommend requiring students to create AWS account and set up EC2 instance and S3 buckets prior to class. Connecting to Jupyter notebook server running in EC2 is a little more complex and can be demoed in class.

### 8. Google Earth Engine

New markdown file 08_google_earth_engine.md created from instructions in PowerPoint lecture notes.

### 9. Visualizing a Half Million Building Footprints on the Web

Some editing of first part of instructions. Added color suggestions for land use choropleth based on APA's Land Based Classification (LBCS) Standards.

This exercise needs review. There is a significant amount of data preparation which delays getting to the interesting part, which is using MapBox Studio to style a map and making the end result publicly available via GitHub Pages. Furthermore the join process takes inordinately long. Running on my laptop (i7 processor), the building-landuse spatial join using an Rtree was taking 5 seconds per building. If I had let it continue to run, it would have taken a month to join all the features. On AWS t2.micro was taking 11 seconds per building. AWS was not only slower, it is not crucial to this exercise *except for the use of tippecanoe to create the mbtiles*. The file sizes also mean that many students who attempted this were running out of space in their EC2 instance, so to make this work you would probably have to put the data in S3 buckets.

A pre-joined shapefile at <https://drive.google.com/file/d/1UZB-1zH0vh37ALYfojm31I9pA_Azkouh/view?usp=sharing> referred to by Xiaojiang in the earlier version of this exercise was not available in Spring 2023.

Note that I was able to (mostly) do the spatial join in a few hours using PostGIS. After uploading and indexing both the buildings and land use layer, I ran the following PostGIS query:

```sql
SELECT b.area, b.base_hgt, b.avg_hgt, b.max_hgt, b.bin, l.c_dig1, l.c_dig2, l.c_dig3, st_transform(b.geom, 4326) 
FROM phl_building_2017 b LEFT JOIN phl_landuse_2016 l 
    ON ST_Intersects(ST_PointOnSurface(b.geom), l.geom)
```

I actually ran the query at the command line in an `ogr2ogr` statement to export directly to GeoJSON. The full statement was:

```sh
ogr2ogr -f "GeoJSON" phl_buildings.geojson PG:"host=localhost port=5433 dbname=gis user=docker password=docker" -sql "SELECT b.area, b.base_hgt, b.avg_hgt, b.max_hgt, b.bin, l.c_dig1, l.c_dig2, l.c_dig3, st_transform(b.geom, 4326) FROM phl_building_2017 b LEFT JOIN phl_landuse_2016 l ON ST_Intersects(ST_PointOnSurface(b.geom), l.geom)"
```

Requiring the students to do the spatial join is a major roadblock. Some possible changes:

1. Provide the students an extract of one neighborhood in Philly prior to doing the spatial join (or perhaps have them clip the data themselves in Python, QGIS, ogr2ogr, or PostGIS, but test to make sure the processing time for the clipping operation is reasonable).
2. Provide the students the joined GeoJSON, and have them use tippecanoe in AWS prior to moving on to MapBox and GitHub Pages.
3. Provide the students the mbtiles and skip using AWS entirely.

### 10. Machine Learning and NAIP

No significant changes.

#### 11. Two Demonstration Notebooks

No changes. Note that necessary package `pysolar` used in shadow-casting-cpu.ipynb is installed in course conda environment. If this exercise is removed or altered, that package should probably be removed from the requirements file.
