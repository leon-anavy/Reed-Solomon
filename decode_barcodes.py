import sys
from composite_RS import barcode_rs_decode
from multiprocessing import Pool
from functools import partial

def main():
    file_in = sys.argv[1]
    try:
        verify_only = bool(int(sys.argv[2]))
    except:
        verify_only = True
    file_out = file_in.replace('.dna','_verify_{}_barcode_decoded.dna'.format(verify_only))
    decode(file_in,file_out,verify_only)

def decode_read_barcode(read, verify_only):
    bc = read[:16]
    bc = bc.replace('N','A')
    decoded_bc = barcode_rs_decode(list(bc), verify_only)
    if decoded_bc is not None:
        if 'AAAA' in decoded_bc or 'CCCC' in decoded_bc or 'GGGG' in decoded_bc or 'TTTT' in decoded_bc:
            return None
        return ''.join(decoded_bc) + read[16:]
    return None

def decode(file_in,file_out,verify_only=True, pooling_val = 500000):
    partial_decode = partial(decode_read_barcode,verify_only=verify_only)
    with open(file_out,'w') as outf:
        outf.write('')
    total = 0
    success = 0
    pool_cnt = 0
    reads = []
    with open(file_in,'r') as fin:
        for idx,read in enumerate(fin):
            if pool_cnt == pooling_val:
                p = Pool(10)
                results = p.map(partial_decode,reads)
                p.close()
                p.join()
                results = [r for r in results if r is not None]
                results = [r for r in results if len(r)    == 152]
                success += len(results)
                print 'total = {}; success = {}; failed = {}'.format(total,success,total-success)
                with open(file_out,'a') as outf:
                    outf.writelines(results)
                reads = []
                pool_cnt = 0
            reads.append(read)
            total += 1
            pool_cnt += 1
        p = Pool(10)
        results = p.map(partial_decode,reads)
        p.close()
        p.join()
        results = [r for r in results if r is not None]
        results = [r for r in results if len(r)    == 152]
        success += len(results)
        print 'total = {}; success = {}; failed = {}'.format(total,success,total-success)
        with open(file_out,'a') as outf:
            outf.writelines(results)
        
if __name__ == "__main__":
    main()
