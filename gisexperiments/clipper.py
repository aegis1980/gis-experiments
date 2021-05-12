
from typing import Tuple
import os

import geopandas as gpd

from gisexperiments import filter_by_extension


def clip(in_shp_dir, out_shp_dir, mask_file_path :str = None, bbox : Tuple= None, save_clipped = True, save_masked = True, reporting = True):

    shp_fps = filter_by_extension(in_shp_dir,'shp')

    if (mask_file_path):
        mask_gdf = gpd.read_file(mask_file_path)
        mask_gdf = mask_gdf.to_crs(epsg=4326)
        bbox = tuple(mask_gdf.total_bounds)

    for shp_fp in shp_fps:
        name_root = shp_fp.split(os.path.sep)[-1][:-4]
        if reporting:
            print('Processing: ' + name_root + 'shp')
            
        clipped_gdf = gpd.read_file(shp_fp,bbox=bbox)

        if save_clipped:
            name = name_root + '_CLIPPED.shp'
            if reporting:
                print(   'saving clipped file')
            clipped_gdf.to_file(os.path.join(out_shp_dir, name))

        if save_masked and mask_file_path:
            if reporting:
                print(   'clipping to mask')
            masked_gdf = gpd.clip(clipped_gdf,mask_gdf)
            name = name_root + '_MASKED.shp'
            if reporting:
                print(   'saving masked file')
            masked_gdf.to_file(os.path.join(out_shp_dir, name))