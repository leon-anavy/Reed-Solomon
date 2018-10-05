import sys
from multiprocessing import Pool
from functools import partial
import random

file_in = sys.argv[1]
alphabet = int(sys.argv[2])
remove_rate = float(sys.argv[3])
mismatch_rate = float(sys.argv[4])
file_out = file_in.replace('.dna','_partial_{}_{}.dna'.format(remove_rate,mismatch_rate))

bc_letters = 'ACGT'
if alphabet == 4:
	letters = 'ACGT'
elif alphabet == 5:
	letters = 'ACGTM'
elif alphabet == 6:
	letters = 'ACGTMK'
else:
	print 'invalid alphabet'
	exit(1)


def modify_oligo(oligo):
	oligo = oligo.rstrip()
	if random.random() < remove_rate:
		return None
	for i in range(16):
		if random.random() < mismatch_rate:
			oligo = oligo[:i] + ''.join(random.sample(bc_letters,1)) + oligo[i+1:]
	for i in range(16,len(oligo)):
		if random.random() < mismatch_rate:
			oligo = oligo[:i] + ''.join(random.sample(letters,1)) + oligo[i+1:]
	return oligo

results = []
with open(file_in,'r') as fin:
	for line in fin:
		results.append(modify_oligo(line))

results = [r for r in results if r is not None]
print 'writing {} oligos from {} to {}'.format(len(results),file_in,file_out)
with open(file_out,'w') as outf:
	outf.writelines([r+'\n' for r in results])