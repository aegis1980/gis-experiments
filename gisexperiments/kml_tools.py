import geopandas as gpd

from gisexperiments import filter_by_extension
import gisexperiments.kml_converter as kmlr


def flatten_geometry(gdf : gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    flattens/merges geometric shapes of import kml and return
    new geodataframe

    Args:
        gdf (gpd.GeoDataFrame): raw df from import KML

    Returns:
        [type]: [description]
    """
    gdf['new_col'] = 0
    gdf_merged = gdf.dissolve(by='new_col')
    return gdf_merged


def kmls2gpd(in_path, merge :bool = True, crs : str = "EPSG:4269") -> gpd.GeoDataFrame:
    """
    load kml files 

    Args:
        in_path (str) : path to directory with kmls in 
        merge (bool) : if true will try and flatten geometry
        crs (str) : default to EPSG:4269 (WSG84) set to None do not want to override.

    """
    kml_fps = filter_by_extension(in_path, 'kml')
    gdfs : gpd.GeoDataFrame = []
    for fp in kml_fps:
        gdf = kmlr.keyholemarkup2x(fp,output='gpd')
        if crs:
            gdf.crs = crs

        if merge:
            gdf_merged = flatten_geometry(gdf)
            if crs:
                gdf_merged.crs = crs
            gdfs.append(gdf_merged)
        else:
            gdfs.append(gdf)
    
    return gdfs


