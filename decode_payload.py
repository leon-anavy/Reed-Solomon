import sys
from composite_RS import rs125_decoder,rs343_decoder,rs64_decoder
from multiprocessing import Pool
from functools import partial

def main():
    file_in = sys.argv[1]
    alphabet = int(sys.argv[2])
    try:
        verify_only = bool(int(sys.argv[3]))
    except:
        verify_only = True
    file_out = file_in.replace('.dna','_verify_{}_payload_decoded.dna'.format(verify_only))
    decode(file_in,alphabet,file_out,verify_only)

def decode_payload(line, rs_decoder, verify_only):
    cnt,oligo = line.split('\t')
    bc = oligo.split(',')[:16]
    payload = oligo.split(',')[16:]
    try:
        decoded_payload = rs_decoder(payload, verify_only)
    except Exception as e:
        # print e
        return None
    if decoded_payload is not None:
        return (cnt, bc + decoded_payload)
    return None

#infile expected as "read_count \t comp-DNA". BC already decoded then will be stiched as is to the edcoded payload
def decode(file_in,alphabet,file_out,verify_only=True, pooling_val = 5000):
    if alphabet == 4:
        partial_decode = partial(decode_payload,rs_decoder=rs64_decoder,verify_only=verify_only)
    elif alphabet == 5:
        partial_decode = partial(decode_payload,rs_decoder=rs125_decoder,verify_only=verify_only)
    elif alphabet == 6:
        partial_decode = partial(decode_payload,rs_decoder=rs343_decoder,verify_only=verify_only)
    else:
        print 'invalid alphabet'
        exit(1)
    print 'decoding {} with alphabet {}; verify only: {}'.format(file_in,alphabet,verify_only)
    with open(file_out,'w') as outf:
        outf.write('')
    total = 0
    success = 0
    pool_cnt = 0
    lines = []
    with open(file_in,'r') as fin:
        for idx,line in enumerate(fin):
            line = line.rstrip()
            if pool_cnt == pooling_val:
                p = Pool(10)
                results = p.map(partial_decode,lines)
                p.close()
                p.join()
                results = [(r[0],r[1]) for r in results if r is not None]
                results = [(cnt,o) for cnt,o in results if len(o) == 144]
                success += len(results)
                print 'total = {}; success = {}; failed = {}'.format(total,success,total-success)
                with open(file_out,'a') as outf:
                    outf.writelines(['{}\t{}\n'.format(cnt,o) for cnt,o in results])
                lines = []
                pool_cnt = 0
            lines.append(line)
            total += 1
            pool_cnt += 1
        p = Pool(10)
        results = p.map(partial_decode,lines)
        p.close()
        p.join()
        results = [r for r in results if r is not None]
        results = [(cnt,o) for cnt,o in results if len(o) == 144]
        success += len(results)
        print 'total = {}; success = {}; failed = {}'.format(total,success,total-success)
        with open(file_out,'a') as outf:
            outf.writelines(['{}\t{}\n'.format(cnt,o) for cnt,o in results])
        
if __name__ == "__main__":
    main()
