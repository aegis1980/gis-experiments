import glob
import os

from . import *
import rasterio
from rasterio.enums import Resampling
from rasterio.merge import merge
from rasterio.plot import show



def test_driver(filePath: str, driver = None):
    ds = rasterio.open(filePath, driver = driver)
    show(ds, cmap='terrain')

def filter_jpgs(path = DATA_ORIGINAL_PATH):
    extension = '*.jpg'

    q = os.path.join(DATA_ORIGINAL_PATH,extension)

    # file paths matching RBG*.jpg
    return glob.glob(q)
    # dataset = rasterio.open('data/aerial/RGB_AX33_10k_0402_2010.jpg')


def mosaic(
        mosaic_res:int = 5,
        src_path:str = DATA_ORIGINAL_PATH, 
        out_path:str = DATA_OUTPUT_PATH, 
        out_name:str = 'mosaic.jpg',
        show_when_done = True
    ) -> str:

    fps = filter_jpgs(src_path)

    srcfiles_to_mosaic = []

    for f in fps:
        src = rasterio.open(f)
        srcfiles_to_mosaic.append(src)

    mosaic, out_trans = merge(srcfiles_to_mosaic, res=mosaic_res)    

    profile = src.profile
    profile.update(transform=out_trans, driver='JPEG')

    out_fp = os.path.join(out_path,out_name)
    with rasterio.open(out_fp, "w", **profile) as dest:
        dest.write(mosaic)

    if show_when_done:
        ds = rasterio.open(out_fp)
        show(ds,cmap = 'terrain')
    
    return out_fp



def downsample(fp: str, full_path = True, factor = 0.1):
    """
    Works on single file okay, 
    but retains same resolution so no good for mosaic
    """
    if not full_path:
        fp = os.path.join(DATA_ORIGINAL_PATH,fp)

    fn = fp.split(os.path.sep)[-1]  
    f_out = os.path.join(DATA_OUTPUT_PATH,fn)

    with rasterio.open(fp) as dataset:

        h= dataset.height * factor
        w= dataset.width * factor

        # resample data to target shape
        data = dataset.read(
            out_shape=(
                dataset.count,
                int(h),
                int(w)
            ),
            resampling=Resampling.cubic
        )

        # scale image transform
        transform = dataset.transform * dataset.transform.scale(
            (dataset.width / data.shape[-1]),
            (dataset.height / data.shape[-2])
        )

        profile = dataset.profile
        profile.update(transform=transform, driver='JPEG', height=h, width=w, crs=dataset.crs)

        with rasterio.open(f_out,'w', **profile) as dst:
            dst.write(data)
           

def save(data, transform, sample_src):
    with rasterio.open(sample_src) as dataset:
        profile = dataset.profile
        profile.update(transform=transform, driver='JPEG')

        with rasterio.open(f_out,'w', **profile) as dst:
            dst.write(data)