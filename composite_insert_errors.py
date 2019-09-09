import sys, itertools, string, random
from scipy.stats import binom
import numpy as np

def main():
    file_in = sys.argv[1]
    alphabet = sys.argv[2]
    max_errors_BC = int(sys.argv[3])
    max_errors_payload = int(sys.argv[4])
    file_out = file_in.replace('.dna','_errors{}_{}.dna'.format(max_errors_BC,max_errors_payload))
    std_alphabet = ['A','C','G','T']
    if alphabet == '4':
        alphabet = ['A','C','G','T']
    elif alphabet == '5':
        alphabet = ['A','C','G','T','M']
    elif alphabet == '6':
        alphabet = ['A','C','G','T','M','K']
    elif alphabet == 'phi10':    
        alphabet = ['A','C','G','T'] + [''.join(p) for p in itertools.product(*[string.ascii_uppercase,]*2)][:252] #A,C,G,T,AA,...,JR
    with open(file_in,'r') as fin:
        results = []
        for l in fin:
            oligo = l.rstrip().split(',')
            bc = oligo[0:16]
            payload = oligo[16:]
            results.append(','.join([insert_errors(bc,std_alphabet,max_errors_BC),insert_errors(payload,alphabet, max_errors_payload)])+'\n')
    with open(file_out,'w') as outf:
        outf.writelines(results)

    
def insert_errors(oligo,alphabet,max_errors):
    N = len(oligo)
    p = 0.5
    # number of errors
    X = binom(N,p)
    Ps = [X.pmf(i) for i in range(max_errors+1)]
    Ps = [p/sum(Ps) for p in Ps]
    errors = np.argmax(np.random.multinomial(1,Ps))
    # error positions
    positions = random.sample(range(N),errors)
    for pos in positions:
        orig = oligo[pos]
        alphabet.remove(orig)
        new = random.sample(alphabet,1)[0]
        oligo[pos] = new
        alphabet.append(orig)
        # print 'replaced in positions {}; original = {}; new = {}'.format(pos,orig,new)
    oligo = ','.join(oligo)
    return oligo
    
        
if __name__ == "__main__":
    main()
