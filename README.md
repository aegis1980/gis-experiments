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

## Experiments

### Expt 1: Mosaic

```bash
python runme_create_mosaic.py
```

Merge/ mosaic all the tiles from sample into single GeoJPEG of managable size, maintaining all GIS meta data of original.

Downsamples from 0.5m res to 2m and merges. Creates ~12MB file.

Note that trying to merge original files without downsample will invariably cause you the following error:

> numpy.core._exceptions.MemoryError: Unable to allocate 250. GiB for an array with shape (3, 345600, 259200) and data type uint8

Files are RGB (3 channels of 256 levels) and merges area's extend is ~173km x130km (345600 x 259200 @ 0.5,0.5m res). A `uint8` is 1 byte:

```bash
[3 x (45600 x 259200) ] x 1 byte = 268.7 gigabytes
```

5/5/21 Update: Previous broke coords. now corrected and seems to work ok.

### Expt 2: KML import

Imports KML files I exported from my Google MyMaps to Geopandas dataframes and merges adjacent polygons.  I checked the KML export in MyMaps, it defaults to KMZ otherwise which works just as well, just KML Is just a textfile so more easily readable & debuggable.

A couple of Python installs/imports. `fiona` from whl included as per previous:

```
pip install shapely, geopandas,pyshp
pip install Fiona-1.8.19-cp38-cp38-win_amd64.whl
```

Then,

```bash
python runme_kml.py
```

Few issues with the KML importer I found [here](https://gist.github.com/linwoodc3/0306734dfe17076dfd34e09660c198c0`):

- Works on the principal that each `<Placemark>`   `<name>`is unique. Names are not unique in the KMLs I exported from MyMaps which result in polygons going missing. I cleaned up by hands in the KML files (renaming duplicates). Could fix in code, someday.
- Importers does not recognise KML `<Folders>` which are how MyMaps 'layers' are distinguished in exported KML.s I exported each layer into separate KML.

### Expt 3: Coordinate systems

Imported KML (from Google MyMaps) does not have a coordinate system - there are many.
