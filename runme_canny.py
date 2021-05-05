# %%
import matplotlib.pyplot as plt
from skimage import feature
import os
import rasterio
from gisexperiments import DATA_OUTPUT_PATH

aerial  = os.path.join(DATA_OUTPUT_PATH,'masked_aerial.jpg')
ds = rasterio.open(aerial)
a = ds.read()

# %%
# Compute the Canny filter of 
edge = []
edges1 = feature.canny(a[2],sigma = 2)

#%%
plt.imshow(edges1, cmap='gray')
# %%

