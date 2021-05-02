# GIS Experiments (Python)

*(Windows, non Anaconda)* Rasterio and GDAL install using whl files included (rather than from pypi). If not using python 3.8, see [here](https://rasterio.readthedocs.io/en/latest/installation.html#windows)

```bash
pip install GDAL-3.2.2-cp38-cp38-win_amd64.whl
pip install rasterio-1.2.3-cp38-cp38-win_amd64.whl
pip install matlibplot
```

## Source data

0.5m resolution aerial images of Auckland. Download from [here](https://data.linz.govt.nz/layer/51769-auckland-05m-rural-aerial-photos-2010-2012/), selecting JPEG format. Download is fairly large (12 gig!) so takes a while.

Unzip into `data/aerial/`

### Expt 1: Mosaic

```bash
runme_create_mosaic.py
```

Merge/ mosaic all the tiles from sample into single GeoJPEG of managable size, maintaining all GIS meta data of original.

Downsamples from 0.5m res to 2m and merges. Creates ~12MB file.

Note that trying to merge original files without downsample will invariably cause you the following error:

> numpy.core._exceptions.MemoryError: Unable to allocate 250. GiB for an array with shape (3, 345600, 259200) and data type uint8

Files are RGB (3 channels of 256 levels) and merges area's extend is ~173km x130km (345600 x 259200 @ 0.5,0.5m res). A `uint8` is 1 byte:

```
[3 x (45600 x 259200) ] x 1 byte = 268.7 gigabytes
```
