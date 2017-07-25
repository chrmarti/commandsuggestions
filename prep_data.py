import gzip
import csv
import numpy as np
# from scipy.sparse import lil_matrix, save_npz
import time

start = time.time()

filename = 'dumps/single-day-20170719.gz'

machines = {}
commands = {}
maxCount = 0

lines = None
with gzip.open(filename, mode='rt') as f:
	csvobj = csv.reader(f, delimiter = ',', quotechar='"')
	lines = list(csvobj)
print('tuples', len(lines))
print('loaded', time.time() - start)

for line in lines:
	machine = line[2]
	command = line[1]
	if command not in commands:
		commands[command] = len(commands)
	if machine not in machines:
		machines[machine] = len(machines)
	maxCount = max(maxCount, int(line[0]))

print('maxCount', maxCount)
print('dims', (len(machines), len(commands)))
print('first run', time.time() - start)

# X = lil_matrix((len(machines), len(commands)), dtype=np.int32)
X = np.zeros((len(machines), len(commands)), dtype=np.int32)
for line in lines:
	machine = line[2]
	command = line[1]
	X[machines[machine], commands[command]] += 1

print('second run', time.time() - start)

import os
if not os.path.exists('data'):
	os.makedirs('data')

from sklearn.externals import joblib
joblib.dump(machines, 'data/machines.pickle')
print('machines saved', time.time() - start)
joblib.dump(commands, 'data/commands.pickle')
print('commands saved', time.time() - start)
# save_npz('data/data.npz', X)
np.savez_compressed('data/data.npz', X=X)
print('data saved', time.time() - start)
