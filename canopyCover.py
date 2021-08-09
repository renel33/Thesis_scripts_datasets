from rasterstats import zonal_stats
import fiona
import rasterio
import rasterio.mask
import pandas as pd
import geopandas as gp
import os
import numpy as np

for r in os.listdir('out_resample1806'):
    imagePath = os.path.join('out_resample1806/' + os.path.basename(r))
    print('Processing: ',imagePath)
    with rasterio.open(imagePath) as src:
        for s in os.listdir('shape'):
            shapePath = os.path.join('shape/' + os.path.basename(s))
            with fiona.open(shapePath, "r") as shapefile:
                shapes = [feature["geometry"] for feature in shapefile]
                out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
                out_meta = src.meta
                out_meta.update({"driver": "GTiff",
                     "height": out_image.shape[1],
                     "width": out_image.shape[2],
                     "transform": out_transform})
                if not os.path.exists('out'):
                    os.makedirs('out')
                out_path = 'out/' + os.path.splitext(r)[0] + os.path.splitext(s)[0] + os.path.splitext(r)[1]
                with rasterio.open(out_path, "w", **out_meta) as dest:
                    dest.write(out_image)

msk = rasterio.open(r"C:\Users\renea\Documents\Thesis\CanopyCover\LAI\LAIclassified1806.tif")
msk = msk.read(1)


for r in os.listdir('out'):
    imagePath = os.path.join('out/' + os.path.basename(r))
    print('Masking: ', imagePath)
    with rasterio.open(imagePath) as src:
        band = src.read(1)
        canopyCover = band.astype(float)*msk.astype(float)
        canopyCover[canopyCover==0] = np.nan
        if not os.path.exists('masked'):
            os.makedirs('masked')
        out_path = 'masked/' + os.path.splitext(r)[0] + '_' + os.path.splitext(r)[1]
        with rasterio.open(out_path, "w", **out_meta) as dest:
            dest.write(canopyCover.astype(rasterio.float32),  1)





#insert shapefile
gdf = gp.read_file('LAI1806.shp')

for r in os.listdir('masked'):
    imagePath = os.path.join('masked/' + os.path.basename(r))
    print(imagePath)
    with rasterio.open(imagePath) as src:
        affine = src.transform
        array = src.read(1)
        df_zonal_stats = pd.DataFrame(zonal_stats(gdf, array, affine=affine, stats='mean'))
    # adding statistics back to original GeoDataFrame
    gdf = pd.concat([gdf, df_zonal_stats], axis=1)


gdf.to_csv('1806LAIcc.csv', index=False)
