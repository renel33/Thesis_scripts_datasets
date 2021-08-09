import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText
import pandas as pd
import geopandas as gp
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error
from sklearn import metrics
from shapely import wkt

#import training data
data = np.genfromtxt('training.csv', delimiter=",", skip_header=1, dtype=float)
datb = pd.read_csv('training.csv', sep=',', dtype=float)

#set x and y
y = data[:,5].reshape(-1, 1)
X = data[:,0:5]

#train test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.35, random_state=42)
#X_train = X_train.T
#X_test = X_test.T
y_train = np.ravel(y_train.T)
y_test = np.ravel(y_test.T)
print(X_test.shape)

#train SVM
clf = make_pipeline(StandardScaler(), SVC(gamma='auto'))
clf.fit(X_train, y_train)

#predict on test data
y_pred = clf.predict(X_test)

#check r2 and RMSE
print('R2: ',clf.score(X_test, y_test))
print('RMSE: ', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))
print('Predicting Class')
#import classification dataset
datc = np.genfromtxt('LNCclassification1806.csv', delimiter=",", skip_header=1, dtype=float)

#predict classification using only x values from classification dataset
K = datc[:,3:8]
K_pred = clf.predict(K)

#write classifications to point shapefile to be imported into arcgis
df = pd.read_csv("LNCclassification1806.csv")
#df = pd.read_file('classification.csv')
df["class"] = K_pred
df.to_csv("LNCclassified1806.csv", index=False)

print('Creating Shapefile')
df = pd.read_csv('LNCclassified1806.csv')
df['geometry'] = df['geometry'].apply(wkt.loads)
gdf = gp.GeoDataFrame(df, crs='epsg:4326')

#gdf.plot("class", legend=True)
#plt.show()

gdf.to_file(driver='ESRI Shapefile',filename="LNCclassified1806.shp")
print('Done!')
