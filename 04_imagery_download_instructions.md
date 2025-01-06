# Raster Data Manipulation - Sample Landsat Data Download Instructions 

 - Visit https://earthexplorer.usgs.gov/, click login, and complete the registration process to create an account. Registration is free but email confirmation required is required, feel free to use your Temple University email account.
 - Login to earth explorer with your account
 - Search for the following scene: `LC08_L2SP_016040_20210317_20210328_02_T1`
   - LC08 refers to Landsat 8, which is the satellite that captured the imagery.
   - L2SP refers to the Level 2 Surface Reflectance product, which means the image has been atmospherically corrected to produce surface reflectance values, a common product for Landsat 8.
   - 016040 is the Path/Row of the Landsat scene. Landsat data is organized into a grid of paths and rows, where 016 is the Path (the longitudinal strip of the scene) and 040 is the Row (the latitudinal strip). Together, this identifies the specific scene within the Landsat grid system.
   - 20210317 represents the acquisition date of the image in YYYYMMDD format, so in this case, the image was captured on March 17, 2021.
   - 20210328: represents the processing date in YYYYMMDD format, which is when the image was processed and made available. In this case, it was processed on March 28, 2021.
   - 02 is the scene number (or version) associated with this particular Landsat image. The scene number is part of the file naming convention used by the USGS to identify different versions of the same scene.
   - T1 indicates the processing level of the data. T1 generally refers to Terrain Corrected data, meaning that geometric corrections have been applied to the image to align it properly to the Earth’s surface.
 - Under Landsat, select the corresponding year, then open the additional criteria tab and input the fields listed above.
  - When you have identified the scene, select Download Options. 
  - Select Level-2 Surface Reflectance Bands, you will a list of bands included in the scene.
  - Download the following bands
    - SR_B2.TIF: Band 2 (Blue)
    - SR_B3.TIF: Band 3 (Green)
    - SR_B4.TIF: Band 4 (Red)
    - SR_B5.TIF: Band 5 (Near-Infrared)
  - Place the files in the `outputs/` folder. Then proceed to  [04_landsat_preprocessing](04_landsat_preprocessing.ipynb)


# Raster Data Manipulation - Sample NAIP Data Download Instructions 

 - Visit https://earthexplorer.usgs.gov/, click login, and complete the registration process to create an account. Registration is free but email confirmation required is required, feel free to use your Temple University email account.

 - Login to earth explorer with your account
 - Select the Data Sets tab
 - Under Aerial Imagery, check the box for NAIP (National Agricultural Imagery Program), then select the button for additional criteria
 - Enter additional criterial such as state, date range, etc. Make sure JP2000 is toggled to YES. Then select the button for Results to execute the search
 - Select a tile that interests you, click Download Options, select to download the Compressed version of the file.  
 - Move the download file to the output/ folder of this repo.
