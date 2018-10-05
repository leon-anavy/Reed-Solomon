import sys
from composite_RS import rs125_decoder,rs343_decoder,rs64_decoder,decode_oligo
from multiprocessing import Pool
from functools import partial

def main():
	file_in = sys.argv[1]
	file_out = file_in.replace('.dna','_decoded.dna')
	alphabet = int(sys.argv[2])
	try:
		verify_only = bool(int(sys.argv[3]))
	except:
		verify_only = True
	decode(in_file,out_file,alphabet,verify_only)
	
def decode(file_in,file_out,alphabet,verify_only=True):
			
	if alphabet == 4:
		partial_decode = partial(decode_oligo,rs_decoder=rs64_decoder,verify_only=verify_only)
	elif alphabet == 5:
		partial_decode = partial(decode_oligo,rs_decoder=rs125_decoder,verify_only=verify_only)
	elif alphabet == 6:
		partial_decode = partial(decode_oligo,rs_decoder=rs343_decoder,verify_only=verify_only)
	else:
		print 'invalid alphabet'
		exit(1)
		
	print 'decoding {} with alphabet {}; verify only: {}'.format(file_in,alphabet,verify_only)

	p = Pool(10)
	with open(file_in,'r') as fin:
		results = p.map(partial_decode,fin)
	total = len(results)
	success = sum(r != None for r in results)
	results = [r for r in results if r is not None]
	print 'total = {}; success = {}; failed = {}'.format(total,success,total-success)
	with open(file_out,'w') as outf:
		outf.writelines([r+'\n' for r in results])
		
if __name__ == "__main__":
	main()