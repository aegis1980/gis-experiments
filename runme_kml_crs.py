"""
Imports 'layers' from from different kml files into geopandas
kml created in Google maps. 
Had to export each 'layer' ('folder' in KML speak) separately since 
importer I found does not take account of folders and I could not be pothered to implement.
"""
#%%
import os
from gisexperiments import DATA_INPUT_PATH, COLORS, DATA_ORIGINAL_AERIALS_PATH, DATA_OUTPUT_PATH, kml_tools

KML_PATH = os.path.join(DATA_INPUT_PATH,'kml')
gdfs = kml_tools.kmls2gpd(KML_PATH)

base = None
i=0
for gdf in gdfs: 
    if not base:
        base = gdf.plot(color = COLORS[i])
    else: 
        gdf.plot(ax=base,color = COLORS[i])
    i +=1


#%%
import rasterio
from rasterio.plot import show
from gisexperiments import DATA_OUTPUT_PATH,DATA_ORIGINAL_AERIALS_PATH
MOSAIC = os.path.join(DATA_OUTPUT_PATH,'mosaic.jpg')
CITY = os.path.join(DATA_ORIGINAL_AERIALS_PATH,'RGB_BA32_10K_0401_2011.jpg')
ds = rasterio.open(MOSAIC)
show(ds)


#%%
#base = show(ds)
new_projection = gdfs[0].to_crs(epsg=2193)
new_projection.plot()

# %%
import geopandas as gpd
import pandas as pd
mask_gdf = gpd.GeoDataFrame(pd.concat(gdfs, ignore_index = True))
mask_gdf = kml_tools.flatten_geometry(mask_gdf)
mask_gdf.crs =  "EPSG:4269"
mask_gdf = mask_gdf.to_crs(epsg=2193) #this is the 
mask_gdf.plot()
#import matplotlib.pyplot as plt
#plt.show()



# %%
mask_gdf.crs
# %%
