import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.externals import joblib

machines = joblib.load('data/machines.pickle')
commands = joblib.load('data/commands.pickle')
X = np.load('data/data.npz')['X']

print('loaded')

nbrs = NearestNeighbors(n_neighbors=2, algorithm='brute').fit(X)
# nbrs = NearestNeighbors(n_neighbors=2, algorithm='ball_tree').fit(X)
distances, indices = nbrs.kneighbors(X[0].reshape(1, -1))

print(distances)
print(indices)
