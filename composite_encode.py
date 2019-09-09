import sys
from composite_RS import rs125,rs343,rs64,rs256, rs3481,encode_oligo
from multiprocessing import Pool
from functools import partial

file_in = sys.argv[1]
file_out = file_in.replace('.dna','_with_RS.dna')
alphabet = sys.argv[2]

if alphabet == '4':
	partial_encode = partial(encode_oligo,rs_coder=rs64)
elif alphabet == '5':
	partial_encode = partial(encode_oligo,rs_coder=rs125)
elif alphabet == '6':
	partial_encode = partial(encode_oligo,rs_coder=rs343)
elif alphabet == 'phi5':
	partial_encode = partial(encode_oligo,rs_coder=rs3481)
elif alphabet == 'phi10':
	partial_encode = partial(encode_oligo,rs_coder=rs256)
else:
	print 'invalid alphabet'
	exit(1)
	
print 'encoding {} with alphabet {}'.format(file_in,alphabet)

p = Pool(10)
with open(file_in,'r') as fin:
    results = p.map(partial_encode,fin)
results = [r for r in results if r != 'not oligo']
total = len(results)
success = sum(r != None for r in results)
results = [r for r in results if r is not None]
print 'total = {}; success = {}; failed = {}'.format(total,success,total-success)
with open(file_out,'w') as outf:
    outf.writelines([','.join(r)+'\n' for r in results])