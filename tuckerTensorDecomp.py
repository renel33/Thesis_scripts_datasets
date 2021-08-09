import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image
from sktensor import dtensor
from sktensor import tucker
from sktensor.core import ttm
import rasterio

plt.rcParams['figure.figsize'] = (25,10)

# Just place the images for corresponding dates below
with rasterio.open("1105_P2_B1_resample_Tucker_mask.tif") as src:
    # Here we need to obatin meta data from original image so that we can reuse it to save the results
    out_meta = src.meta.copy()
    profile = src.profile
    print(out_meta['transform'])
    im1 = src.read(1)

with rasterio.open("3005_P2_B1_resample_Tucker_mask.tif") as src:
    out_meta = src.meta.copy()
    print(out_meta['transform'])
    im2 = src.read(1)

with rasterio.open("3105_1030_B1_resample_Tucker_mask.tif") as src:
    out_meta = src.meta.copy()
    print(out_meta['transform'])
    im3 = src.read(1)

x = np.min(list(map(lambda x:x.shape[0], [im1, im2, im3])))
y = np.min(list(map(lambda x:x.shape[1], [im1, im2, im3])))
im1 = im1[:x,:y]
im2 = im2[:x,:y]
im3 = im3[:x,:y]

print(np.array(im1).shape)
print(np.array(im2).shape)
print(np.array(im3).shape)
IM = np.stack((im1, im2, im3), axis=0)
print(IM.shape)
# Make sure it stacked in the way X is described in the equation/or the X component as per graph. It may be requiered to reshape or use axis =1.

# Fixing edge values - should not be neede if images are croped correctly
#IM[0] = np.where(IM[0] == 0, -32767.0, IM[0])
#IM[1] = np.where(IM[1] == 0, -32767.0, IM[1])
#IM[2] = np.where(IM[2] == 0, -32767.0, IM[2])

X = dtensor(np.array(IM))
# Only 1 and 2 are valid inputs when 3 images are used, 1 means 'more' shadow/sun is removed while 2 will keep some
# you should inspect the results to pick a desired value
R = 2
# Q and P should aproximetly keep the same aspect ratio as a original images - IMPORTANT
# The higher the value the more data is preserved during the decomposition process
# Mostly likely it should get better while increasing a number till it reaches a point of saturation
# where slightly misaligned pixels will introduce noise grater then benefits of keeping data about low variance
# simillarly as PCA does ;)
# That is another parameter dependent on particular image and alignment precision,
# you should try a few different values and compare the model performance on it.
# It should be possible to find common values for all of our data as I asume alignment performance, sieze etc are quite consistant
Q = 2552
P = 1485

# Parameters to be further cusstomized if needed
#I think it was designed with smaller matriceses then we have in mind so lilely needs to be reised, especially when high values of Q and P are used
#__DEF_MAXITER = 500
#__DEF_INIT = 'nvecs'
#__DEF_CONV = 1e-7
G, U = tucker.hooi(X, [R, Q, P], init='nvecs')

print(G.shape)
print(len(U))
print(len(U[0]))
print(len(U[1]))
print(len(U[2]))
#print(G)
#print(U)

# Reverse transformation to obtain cloud free image
# Note that that method will result with all input images to be modified, therfore all of them should be used insted of original ones(keeping some hand picked 'cloud free images' in the data set for further ML is not a good idea)
A = ttm(G, U)
print(A.shape)

#plt.subplot(1, 2, 1)
#plt.imshow(np.array(IM[0]), cmap=plt.cm.gray)

#plt.subplot(1, 2, 2)
#plt.imshow(np.array(A[0]), cmap=plt.cm.gray)

#plt.show()

with rasterio.open('out/MayDate1B1.tif', 'w', **profile) as dst:
    dst.write(A[0].astype(rasterio.float32), 1)

with rasterio.open('out/MayDate2B1.tif', 'w', **profile) as dst:
    dst.write(A[1].astype(rasterio.float32), 1)

with rasterio.open('out/MayDate3B1.tif', 'w', **profile) as dst:
    dst.write(A[2].astype(rasterio.float32), 1)
