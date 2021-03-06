
from gisexperiments import DATA_ORIGINAL_AERIALS_PATH,DATA_OUTPUT_PATH
from gisexperiments import mosaic

mosaic.mosaic(
    mosaic_res= 5, #m (original files are 0.5m resolution)
    src_path = DATA_ORIGINAL_AERIALS_PATH,
    out_path= DATA_OUTPUT_PATH, 
    out_name= 'mosaic.jpg',
    show_when_done= True
)
