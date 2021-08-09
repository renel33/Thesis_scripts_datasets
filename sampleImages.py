
import fiona
from rasterstats import zonal_stats
import rasterio
import rasterio.mask
import pandas as pd
import geopandas as gp
import os



gdf = gp.read_file('classifiedPoint.shp')

for r in os.listdir('1806'):
    imagePath = os.path.join('1806/' + os.path.basename(r))
    print(imagePath)
    with rasterio.open(imagePath) as src:
        affine = src.transform
        array = src.read(1)
        df_zonal_stats = pd.DataFrame(zonal_stats(gdf, array, affine=affine, stats='mean'))
    # adding statistics back to original GeoDataFrame
    gdf = pd.concat([gdf, df_zonal_stats], axis=1)
    print('Done!')

gdf.to_csv('LNCclassification1806.csv', index=False)
