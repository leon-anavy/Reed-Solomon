import ff16, ff64, ff125, ff343, ff125, ff256, ff3481, rs
import itertools, string

### fix barcode
barcode_rs_coder = rs.RSCoder(GFint=ff16.GFint,k=7,n=8)
ff16_trantab = {''.join(vv):i for i,vv in enumerate(itertools.product('ACGT','ACGT'))}
ff16_rev_trantab = {i:vv for vv,i in ff16_trantab.items()}

def barcode_rs(barcode):
    message = barcode[2:]
    message_int = [ff16_trantab[''.join(message[i:i+2])] for i in range(0,14,2)]
    codeword = barcode_rs_coder.encode(message_int)
    coded_barcode = [vv for v in codeword for vv in ff16_rev_trantab[v]]
    return coded_barcode
    
def barcode_rs_decode(barcode, verify_only = True):
    received_int = [ff16_trantab[''.join(barcode[i:i+2])] for i in range(0,16,2)]
    if barcode_rs_coder.verify(received_int):
        return ['A','A'] + barcode[0:14]
    elif not verify_only:
        decoded_int = barcode_rs_coder.decode(received_int)
        decoded_message = [vv for v in decoded_int for vv in ff16_rev_trantab[v]]
        return ['A','A'] + decoded_message
    return None

### rs3481
rs3481_coder = rs.RSCoder(GFint=ff3481.GFint,k=64,n=68)
alphabet56 = ['A','C','G','T'] + [''.join(p) for p in itertools.product(*[string.ascii_uppercase,]*2)][:52] #A,C,G,T,AA,...,BZ
ff3481_trantab = {','.join(vv):i for i,vv in enumerate(itertools.product(alphabet56,alphabet56))}
ff3481_rev_trantab = {i:vv for vv,i in ff3481_trantab.items()}
def rs3481(payload):
    # print ff3481_trantab
    bla = [','.join(payload[i:i+2]) for i in range(0,len(payload),2)]
    message_int = [ff3481_trantab[','.join(payload[i:i+2])] for i in range(0,len(payload),2)]
    codeword = rs3481_coder.encode(message_int)
    coded_message = [ff3481_rev_trantab[v].split(',') for v in codeword]
    coded_message = [vv for v in coded_message for vv in v]
    return coded_message

def rs3481_decoder(received, verify_only = True):
    received_int = [ff3481_trantab[','.join(received[i:i+2])] for i in range(0,len(received),2)]
    decoded_message = 'AAAA'
    if rs3481_coder.verify(received_int):
        decoded_message = [ff3481_rev_trantab[v] for v in received_int[0:-4]]
    elif not verify_only:
        decoded_int = rs3481_coder.decode(received_int)
        decoded_message = [ff3481_rev_trantab[v] for v in decoded_int]
    if len(decoded_message) == 64:
        return decoded_message
    return None

    
### rs256
rs256_coder = rs.RSCoder(GFint=ff256.GFint,k=130,n=136)
alphabet256 = ['A','C','G','T'] + [''.join(p) for p in itertools.product(*[string.ascii_uppercase,]*2)][:252] #A,C,G,T,AA,...,JR
ff256_trantab = {vv:i for i,vv in enumerate(alphabet256)}
ff256_rev_trantab = {i:vv for vv,i in ff256_trantab.items()}
def rs256(payload):
    payload_int = [ff256_trantab[l] for l in payload]
    codeword = rs256_coder.encode(payload_int)
    coded_message = [ff256_rev_trantab[v] for v in codeword]
    return coded_message

def rs256_decoder(received, verify_only = True):
    received_int = [ff256_trantab[l] for l in received]
    decoded_message = 'AAAA'
    if rs256_coder.verify(received_int):
        decoded_message = [ff256_rev_trantab[v] for v in received_int[:-6]]
    elif not verify_only:
        decoded_int = rs256_coder.decode(received_int)
        decoded_message = [ff256_rev_trantab[v] for v in decoded_int]
    if len(decoded_message) == 130:
        return decoded_message
    return None

    
### rs343
rs343_coder = rs.RSCoder(GFint=ff343.GFint,k=43,n=45)
ff343_trantab = {','.join(vv):i for i,vv in enumerate(itertools.product('ACGTMK','ACGTMK','ACGTMK'))}
ff343_rev_trantab = {i:vv for vv,i in ff343_trantab.items()}

def rs343(payload):
    message = payload+['K',]
    message_int = [ff343_trantab[','.join(message[i:i+3])] for i in range(0,len(message),3)]
    codeword = rs343_coder.encode(message_int)
    coded_message = [ff343_rev_trantab[v].split(',') for v in codeword]
    coded_message = [vv for v in coded_message for vv in v]
    return coded_message

def rs343_decoder(received, verify_only = True):
    received_int = [ff343_trantab[','.join(received[i:i+3])] for i in range(0,len(received),3)]
    decoded_message = 'AAAA'
    if rs343_coder.verify(received_int):
        decoded_message = [ff343_rev_trantab[v] for v in received_int[0:-2]]
    elif not verify_only:
        decoded_int = rs343_coder.decode(received_int)
        decoded_message = [ff343_rev_trantab[v] for v in decoded_int]
    decoded_message = [vv for v in decoded_message for vv in v.split(',')]
    if len(decoded_message) == 43*3 and decoded_message[-1] == 'K':
        return decoded_message[:-1]
    return None

### rs125
rs125_coder = rs.RSCoder(GFint=ff125.GFint,k=43,n=45)
ff125_trantab = {''.join(vv):i for i,vv in enumerate(itertools.product('ACGTM','ACGTM','ACGTM'))}
ff125_rev_trantab = {i:vv for vv,i in ff125_trantab.items()}

def rs125(payload):
    message = payload+'M'
    message_int = [ff125_trantab[''.join(message[i:i+3])] for i in range(0,len(message),3)]
    codeword = rs125_coder.encode(message_int)
    coded_message = ''.join([ff125_rev_trantab[v] for v in codeword])
    return coded_message

def rs125_decoder(received, verify_only = True):
    received_int = [ff125_trantab[''.join(received[i:i+3])] for i in range(0,len(received),3)]
    decoded_message = 'AAAA'
    if rs125_coder.verify(received_int):
        decoded_message = ''.join([ff125_rev_trantab[v] for v in received_int[0:-2]])
    elif not verify_only:
        decoded_int = rs125_coder.decode(received_int)
        decoded_message = ''.join([ff125_rev_trantab[v] for v in decoded_int])
    if len(decoded_message) == 43*3 and decoded_message[-1] == 'M':
        return decoded_message[:-1]
    return None

### rs64
rs64_coder = rs.RSCoder(GFint=ff64.GFint,k=43,n=45)
ff64_trantab = {''.join(vv):i for i,vv in enumerate(itertools.product('ACGT','ACGT','ACGT'))}
ff64_rev_trantab = {i:vv for vv,i in ff64_trantab.items()}

def rs64(payload):
    message = payload+'C'
    message_int = [ff64_trantab[''.join(message[i:i+3])] for i in range(0,len(message),3)]
    codeword = rs64_coder.encode(message_int)
    coded_message = ''.join([ff64_rev_trantab[v] for v in codeword])
    return coded_message

def rs64_decoder(received, verify_only = True):
    received_int = [ff64_trantab[''.join(received[i:i+3])] for i in range(0,len(received),3)]
    decoded_message = 'AAAA'
    if rs64_coder.verify(received_int):
        decoded_message = ''.join([ff64_rev_trantab[v] for v in received_int[0:-2]])
    elif not verify_only:
        decoded_int = rs64_coder.decode(received_int)
        decoded_message = ''.join([ff64_rev_trantab[v] for v in decoded_int])
    if len(decoded_message) == 43*3 and decoded_message[-1] == 'C':
        return decoded_message[:-1]
    return None

### all
def encode_oligo(oligo, rs_coder):
    if oligo.startswith('>'):
        return 'not oligo'
    ll = oligo.rstrip().split(',')
    barcode = ll[:16]
    coded_barcode = barcode_rs(barcode)
    payload = ll[16:]
    try:
        coded_payload = rs_coder(payload)
    except Exception as e:
        # print e, e.args
        return None
    return coded_barcode+coded_payload

def decode_oligo(oligo, rs_decoder, verify_only = True):
    ll = oligo.rstrip().split(',')
    barcode = ll[:16]
    try:
        decoded_barcode = barcode_rs_decode(barcode,verify_only)
    except Exception as e:
        #print e, e.args
        return None
    payload = ll[16:]
    try:
        decoded_payload = rs_decoder(payload,verify_only)
    except Exception as e:
        #print e, e.args
        return None
    try:
        return decoded_barcode+decoded_payload
    except Exception as e:
        #print e, e.args
        return None
