#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 18:52:14 2023

@author: lee
"""

import os
import geopandas as gpd
from shapely.geometry.polygon import Polygon
from shapely.geometry.multipolygon import MultiPolygon

def shp_to_gpkg(shp_name, gpkg_name = None):
    
    if gpkg_name is None:
        gpkg_name = os.path.splitext(os.path.basename(shp_name))[0] + ".gpkg"
        
    # Load shapefile
    gdf = gpd.read_file(shp_name)
    
    # Promote to multi
    gdf["geometry"] = [MultiPolygon([feature]) if type(feature) == Polygon \
       else feature for feature in gdf["geometry"]]

    # Write to Geopackage
    gdf.to_file(os.path.join(os.path.dirname(shp_name), gpkg_name), driver = "GPKG")

for current_folder, folders, files in os.walk("."):
    for file in files:
        if file.endswith(".shp"):
            shp_to_gpkg(os.path.join(current_folder, file))
            # print(os.path.basename(os.path.join(current_folder, file)))
            # print(os.path.exists(os.path.join(current_folder, file)))
            
            
    