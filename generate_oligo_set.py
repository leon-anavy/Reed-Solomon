import sys
import random

file_in = sys.argv[1]
file_out = file_in.replace('.dna','_final.dna')
with open(file_in,'r') as fin:
	results = fin.readlines()
results = [r.rstrip() for r in results]
try:
	N = int(sys.argv[2])
except:
	N = len(results)

random.shuffle(results)

print 'writing {} oligos from {}'.format(N,file_in)
with open(file_out,'w') as outf:
	outf.writelines([r+'\n' for r in results[:N]])