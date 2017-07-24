import gzip
import csv
import numpy as np

filename = 'dumps/single-day-20170719.gz'

machines = {}
commands = {}
maxCount = 0
with gzip.open(filename, mode='rt') as f:
	csvobj = csv.reader(f, delimiter = ',', quotechar='"')
	for line in csvobj:
		machine = line[2]
		command = line[1]
		if command not in commands:
			commands[command] = len(commands)
		if machine not in machines:
			machines[machine] = len(machines)
		maxCount = max(maxCount, int(line[0]))

print('maxCount', maxCount)

X = np.zeros((len(machines), len(commands)), dtype=np.int32)
with gzip.open(filename, mode='rt') as f:
	csvobj = csv.reader(f, delimiter = ',', quotechar='"')
	for line in csvobj:
		machine = line[2]
		command = line[1]
		X[machines[machine], commands[command]] += 1

import os
if not os.path.exists('data'):
	os.makedirs('data')

from sklearn.externals import joblib
joblib.dump(machines, 'data/machines.pickle')
joblib.dump(commands, 'data/commands.pickle')
np.savez_compressed('data/data.npz', X=X)
