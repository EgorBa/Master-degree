import numpy as np
import pandas as pd

import plotly.express as px
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

df = pd.read_csv('new_data.csv')
X = list()
for col in df:
    X.append(df[col])
X.pop()
X = pd.DataFrame(X).transpose()

pipeline = Pipeline([('scaling', StandardScaler()), ('pca', PCA(n_components=2))])
X = pipeline.fit_transform(X)
Y = df.iloc[:, -1]
new_X = list()
new_Y = list()
for (index, (x, y)) in enumerate(X):
    if -5 <= x <= 5 and -5 <= y <= 5:
        new_X.append([x, y])
        new_Y.append(Y[index])

fig = px.scatter(new_X, x=0, y=1, color=new_Y)
fig.show()
