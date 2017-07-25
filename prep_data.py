import gzip
import csv
import os

import numpy as np
from scipy.sparse import lil_matrix, save_npz
import time

start = time.time()

# filenames = [ 'dumps/part-20170720.gz' ]
# filenames = [ 'dumps/single-day-20170720.gz' ]
filenames = [ 'dumps/week/' + f for f in os.listdir('dumps/week') ]

machines = {}
commands = {}
maxCount = 0

lines = []
for filename in filenames:
	with gzip.open(filename, mode='rt') as f:
		csvobj = csv.reader(f, delimiter = ',', quotechar='"')
		lines += csvobj
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

X = lil_matrix((len(machines), len(commands)), dtype=np.int32)
# X = np.zeros((len(machines), len(commands)), dtype=np.int32)
for line in lines:
	machine = line[2]
	command = line[1]
	X[machines[machine], commands[command]] += int(line[0])

print('second run', time.time() - start)

import os
if not os.path.exists('data'):
	os.makedirs('data')

from sklearn.externals import joblib
joblib.dump(machines, 'data/machines.pickle')
print('machines saved', time.time() - start)
joblib.dump(commands, 'data/commands.pickle')
print('commands saved', time.time() - start)
csr = X.tocsr()
save_npz('data/data.npz', csr)
# np.savez_compressed('data/data.npz', X=X)
print('data saved', time.time() - start)
