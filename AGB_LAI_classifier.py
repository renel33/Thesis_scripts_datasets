
import fiona
from rasterstats import zonal_stats
import rasterio
import rasterio.mask
import pandas as pd
import geopandas as gp
import os


#create geodataframe from point shapefile
gdf = gp.read_file('shapeFiles/point1807.shp')

#sample all pixels for each band (orthomosaic) in folder
for r in os.listdir('raw/1807p2'):
    imagePath = os.path.join('raw/1807p2/' + os.path.basename(r))
    print(imagePath)
    with rasterio.open(imagePath) as src:
        affine = src.transform
        array = src.read(1)
        df_zonal_stats = pd.DataFrame(zonal_stats(gdf, array, affine=affine, stats='mean'))
    # adding statistics back to original GeoDataFrame
    gdf = pd.concat([gdf, df_zonal_stats], axis=1)
    print('Done!')
#export sampled pixels (model input data) as csv
gdf.to_csv('AGBpoint1807p2.csv', index=False)
