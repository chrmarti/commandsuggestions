import sys
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.externals import joblib
from scipy.sparse import load_npz
import time

start = time.time()

machines = joblib.load('data/machines.pickle')
print('machines loaded', time.time() - start)
commands = joblib.load('data/commands.pickle')
print('commands loaded', time.time() - start)
X = load_npz('data/data.npz')
X.sort_indices() # Avoids https://github.com/scikit-learn/scikit-learn/issues/6614
print('data loaded', time.time() - start)

nbrs = NearestNeighbors(n_neighbors=100, algorithm='brute', n_jobs=1).fit(X) # n_jobs=-1 ends in 'No space left on device' in local Docker
print('fit', time.time() - start)

commands_inv = { v: k for k, v in commands.items() }
print('commands_inv', time.time() - start)

def compute_suggestions(machine_id):
	if machine_id not in machines:
		return []
	
	machine_index = machines[machine_id]
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
				candidates[cindex]['count'] += int(count)
	print('candidates', time.time() - start)

	result = sorted(list(candidates.values()), key=lambda k: -k['count'])
	result_ids = [ {
		'command': commands_inv[candidate['index']],
		'count': candidate['count']
	} for candidate in result ]
	print('result', time.time() - start)
	return {
		'n_of_commands': int(input.sum()),
		'suggestions': result_ids
	}

if __name__ == '__main__' and len(sys.argv) == 2:
	machine_id = sys.argv[1]
	result = compute_suggestions(machine_id)
	print('n_of_commands', result['n_of_commands'])
	for suggestion in result['suggestions']:
		print(suggestion['command'], suggestion['count'])
else:
	from flask import Flask, request, jsonify

	app = Flask(__name__)

	@app.route('/command_suggestions')
	def index():
		machine_id = request.args.get('machine_id')
		return jsonify(compute_suggestions(machine_id))
	
	if __name__ == '__main__':
		app.run()

# curl http://localhost:5000/command_suggestions?machine_id=ae7bbfbc14df1cb2de192c37f788d7db0ddba3da0906015e8e4b43c8e56a281c
