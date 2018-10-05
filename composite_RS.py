import ff16, ff64, ff125, ff343, rs
import itertools

### fix barcode
barcode_rs_coder = rs.RSCoder(GFint=ff16.GFint,k=7,n=8)
ff16_trantab = {''.join(vv):i for i,vv in enumerate(itertools.product('ACGT','ACGT'))}
ff16_rev_trantab = {i:vv for vv,i in ff16_trantab.items()}

def barcode_rs(barcode):
	message = barcode[2:]
	message_int = [ff16_trantab[''.join(message[i:i+2])] for i in range(0,14,2)]
	codeword = barcode_rs_coder.encode(message_int)
	coded_barcode = ''.join([ff16_rev_trantab[v] for v in codeword])
	return coded_barcode
	
def barcode_rs_decode(barcode, verify_only = True):
	received_int = [ff16_trantab[''.join(barcode[i:i+2])] for i in range(0,16,2)]
	if barcode_rs_coder.verify(received_int):
		return 'AA' + barcode[0:14]
	elif not verify_only:
		decoded_int = barcode_rs_coder.decode(received_int)
		decoded_message = ''.join([ff16_rev_trantab[v] for v in decoded_int])
		return 'AA' + decoded_message
	return None

### rs343
rs343_coder = rs.RSCoder(GFint=ff343.GFint,k=43,n=45)
ff343_trantab = {''.join(vv):i for i,vv in enumerate(itertools.product('ACGTMK','ACGTMK','ACGTMK'))}
ff343_rev_trantab = {i:vv for vv,i in ff343_trantab.items()}

def rs343(payload):
	message = payload+'K'
	message_int = [ff343_trantab[''.join(message[i:i+3])] for i in range(0,len(message),3)]
	codeword = rs343_coder.encode(message_int)
	coded_message = ''.join([ff343_rev_trantab[v] for v in codeword])
	return coded_message

def rs343_decoder(received, verify_only = True):
	received_int = [ff343_trantab[''.join(received[i:i+3])] for i in range(0,len(received),3)]
	decoded_message = 'AAAA'
	if rs343_coder.verify(received_int):
		decoded_message = ''.join([ff343_rev_trantab[v] for v in received_int[0:-2]])
	elif not verify_only:
		decoded_int = rs343_coder.decode(received_int)
		decoded_message = ''.join([ff343_rev_trantab[v] for v in decoded_int])
	if decoded_message[-1] == 'K':
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
	if decoded_message[-1] == 'M':
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
	if decoded_message[-1] == 'C':
		return decoded_message[:-1]
	return None

### all
def encode_oligo(oligo, rs_coder):
	if oligo.startswith('>'):
		return 'not oligo'
	ll = oligo.rstrip()
	barcode = ll[:16]
	coded_barcode = barcode_rs(barcode)
	payload = ll[16:]
	try:
		coded_payload = rs_coder(payload)
	except:
		return None
	return coded_barcode+coded_payload

def decode_oligo(oligo, rs_decoder, verify_only = True):
	ll = oligo.rstrip()
	barcode = ll[:16]
	try:
		decoded_barcode = barcode_rs_decode(barcode,verify_only)
	except:
		return None
	payload = ll[16:]
	try:
		decoded_payload = rs_decoder(payload,verify_only)
	except Exception as e:
		return None
	try:
		return decoded_barcode+decoded_payload
	except:
		return None
