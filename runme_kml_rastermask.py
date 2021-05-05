"""
Crops/ masks aerial maps raster to data bounds of KML.
"""

# as per runme_kml.py

import os
from gisexperiments import DATA_INPUT_PATH, kml_tools

KML_PATH = os.path.join(DATA_INPUT_PATH,'kml')
gdfs = kml_tools.kmls2gpd(KML_PATH)

# for some reason putting these imports into front of the last operation breaks something.
# hard to beleive, I know. 

import rasterio
import rasterio.mask
import geopandas as gpd
import pandas as pd
import fiona
from gisexperiments import DATA_OUTPUT_PATH

MOSAIC_AERIAL_PATH = os.path.join(DATA_OUTPUT_PATH,'mosaic.jpg')
MASKED_AERIAL_PATH = os.path.join(DATA_OUTPUT_PATH,'masked_aerial.jpg')

#
mask_gdf = gpd.GeoDataFrame(pd.concat(gdfs, ignore_index = True))
mask_gdf = kml_tools.flatten_geometry(mask_gdf)
mask_gdf = mask_gdf.to_crs(epsg=2193) 

mask_fp = os.path.join(DATA_OUTPUT_PATH,'mask.shp')
mask_gdf.to_file(mask_fp)

with fiona.open(mask_fp,  "r") as shapefile:
    shapes = [feature["geometry"] for feature in shapefile]

with rasterio.open(MOSAIC_AERIAL_PATH) as src:
    out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
    out_meta = src.meta.copy()

out_meta.update({"driver": "JPEG",
                "height": out_image.shape[1],
                "width": out_image.shape[2],
                "transform": out_transform})

with rasterio.open(MASKED_AERIAL_PATH, "w", **out_meta) as dest:
    dest.write(out_image)
