from rasterstats import zonal_stats
import fiona
import rasterio
import rasterio.mask
import pandas as pd
import geopandas as gp
import os

# Clip to shapefile
for r in os.listdir('1105'):
    imagePath = os.path.join('1105/' + os.path.basename(r))
    print(imagePath)
    with rasterio.open(imagePath) as src:
        for s in os.listdir('shapeFile'):
            shapePath = os.path.join('shapeFile/' + os.path.basename(s))
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
                out_path = 'out/' + os.path.splitext(r)[0] + '_' + os.path.splitext(s)[0] + os.path.splitext(r)[1]
                with rasterio.open(out_path, "w", **out_meta) as dest:
                    dest.write(out_image)

#insert shapefile
gdf = gp.read_file('LAI1806.shp')

for r in os.listdir('out'):
    imagePath = os.path.join('out/' + os.path.basename(r))
    print(imagePath)
    with rasterio.open(imagePath) as src:
        affine = src.transform
        array = src.read(1)
        df_zonal_stats = pd.DataFrame(zonal_stats(gdf, array, affine=affine, stats='mean'))
    # adding statistics back to original GeoDataFrame
    gdf = pd.concat([gdf, df_zonal_stats], axis=1)


gdf.to_csv('1105.csv', index=False)
