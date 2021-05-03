"""
Imports 'layers' from from different kml files into geopandas
kml created in Google maps. 
Had to export each 'layer' ('folder' in KML speak) separately since 
importer I found does not take account of folders and I could not be pothered to implement.
"""


import os
from gisexperiments import DATA_INPUT_PATH,DATA_OUTPUT_PATH, filter_by_extension, COLORS
import gisexperiments.kml_converter as kmlr

KML_PATH = os.path.join(DATA_INPUT_PATH,'kml')


kml_fps = filter_by_extension(KML_PATH, 'kml')

base = None

i=0
for fp in kml_fps:
    print (fp)
    gdf = kmlr.keyholemarkup2x(fp,output='gpd')
    gdf['new_col'] = 0
    gdf_new = gdf.dissolve(by='new_col')
    if not base:
        base = gdf_new.plot(color = COLORS[i])
    else: 
        gdf_new.plot(ax=base,color = COLORS[i])
    i +=1


import matplotlib.pyplot as plt
plt.show()