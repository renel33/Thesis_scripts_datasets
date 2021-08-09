#VIS calculations

import numpy
import rasterio
from rasterio.plot import show
import os
import math

rasters = os.listdir('1207')
print(rasters)
#imagePath = os.path.join('1105/' + os.path.basename(r))

with rasterio.open(os.path.join('1207/' + rasters[1])) as src2:
    B2 = src2.read(1)

with rasterio.open(os.path.join('1207/' + rasters[2])) as src3:
    B3 = src3.read(1)

with rasterio.open(os.path.join('1207/' + rasters[3])) as src4:
    B4 = src4.read(1)

with rasterio.open(os.path.join('1207/' + rasters[4])) as src5:
    B5 = src5.read(1)

#kwargs
kwargs = src2.meta
kwargs.update(
    dtype=rasterio.float32,
    count=1,
    compress='lzw')

#ndvi
ndvi = numpy.zeros(B3.shape, dtype=rasterio.float32)
ndvi = (B5.astype(float)-B3.astype(float))/(B5+B3)
#show(ndvi)
with rasterio.open('1207/NDVI.tif', 'w', **kwargs) as dst:
    dst.write_band(1, ndvi.astype(rasterio.float32))

#ndre
ndre = numpy.zeros(B4.shape, dtype=rasterio.float32)
ndre = (B5.astype(float)-B4.astype(float))/(B5+B4)
#show(ndre)
with rasterio.open('1207/NDRE.tif', 'w', **kwargs) as dst:
    dst.write_band(1, ndre.astype(rasterio.float32))

#cigr
cigr = numpy.zeros(B4.shape, dtype=rasterio.float32)
cigr = (B5.astype(float)/B2.astype(float))-1
#show(cigr)
with rasterio.open('1207/cigr.tif', 'w', **kwargs) as dst:
    dst.write_band(1, cigr.astype(rasterio.float32))

#cire
cire = numpy.zeros(B4.shape, dtype=rasterio.float32)
cire = (B5.astype(float)/B4.astype(float))-1
#show(cire)
with rasterio.open('1207/cire.tif', 'w', **kwargs) as dst:
    dst.write_band(1, cire.astype(rasterio.float32))

#mtci
mtci = numpy.zeros(B4.shape, dtype=rasterio.float32)
mtci = (B5.astype(float)-B4.astype(float))/(B4-B3)
#show(mtci)
with rasterio.open('1207/mtci.tif', 'w', **kwargs) as dst:
    dst.write_band(1, mtci.astype(rasterio.float32))

#rdvi
rdvi = numpy.zeros(B4.shape, dtype=rasterio.float32)
rdvi = (B5.astype(float)-B3.astype(float))/(B5+B3)**0.5
with rasterio.open('1207/rdvi.tif', 'w', **kwargs) as dst:
    dst.write_band(1, rdvi.astype(rasterio.float32))
