import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.externals import joblib
from scipy.sparse import load_npz
import time

start = time.time()

machine_id = ''

machines = joblib.load('data/machines.pickle')
machine_index = machines[machine_id]
print('machines loaded', time.time() - start)
commands = joblib.load('data/commands.pickle')
print('commands loaded', time.time() - start)
# X = np.load('data/data.npz')['X']
X = load_npz('data/data.npz')
X.sort_indices() # Avoids https://github.com/scikit-learn/scikit-learn/issues/6614
print('data loaded', time.time() - start)

nbrs = NearestNeighbors(n_neighbors=100, algorithm='brute', n_jobs=-1).fit(X)
# nbrs = NearestNeighbors(n_neighbors=2, algorithm='ball_tree').fit(X)
print('fit', time.time() - start)
input = X[machine_index]
distances, mindices = nbrs.kneighbors(input)

print('distances', distances)
print('mindices', mindices)
print('kneighbors', time.time() - start)

candidates = {}
for mindex in mindices[0][1:]:
	candidate = X[mindex].tocoo()
	for cindex, count in zip(candidate.col, candidate.data):
		if not input[0, cindex]:
			if cindex not in candidates:
				candidates[cindex] = { 'index' : cindex, 'count' : 0 }
			candidates[cindex]['count'] += count
print('candidates', time.time() - start)

commands_inv = { v: k for k, v in commands.items() }
print('commands_inv', time.time() - start)

result = sorted(list(candidates.values()), key=lambda k: -k['count'])
for candidate in result:
	print(commands_inv[candidate['index']], candidate['count'])
print('result', time.time() - start)
