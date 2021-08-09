from osgeo import gdal
import os

#Iterate through directory
for r in os.listdir('3005'):
    imagePath = os.path.join('3005/' + os.path.basename(r))
    #Create out file
    if not os.path.exists('out_resample3005'):
        os.makedirs('out_resample3005')
    out_path = 'out_resample3005/' + os.path.splitext(r)[0] + '_resample' + os.path.splitext(r)[1]
    #Resample images
    ds = gdal.Translate(out_path, imagePath, xRes=0.1, yRes=0.1, resampleAlg="bilinear", format='GTiff')
    print('Finished resampling: ', imagePath)
