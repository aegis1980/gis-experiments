"""
Imports 'layers' from from different kml files into geopandas
kml created in Google maps. 
Had to export each 'layer' ('folder' in KML speak) separately since 
importer I found does not take account of folders and I could not be pothered to implement.
"""

import os
from gisexperiments import DATA_INPUT_PATH, COLORS, kml_tools

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


import matplotlib.pyplot as plt
plt.show()

