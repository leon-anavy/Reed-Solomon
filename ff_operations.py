# encoding: UTF-8

from polynomial import Polynomial
import random

""" finds a generator element of a simple finite field
for each field element go over all powers to see if the order os the size of the field-1
""" 
def find_generator_element(z):
    for a in range(2,z):
        for deg in range(1,z-1):
            if a ** deg % z == 1:
                break
        if a ** (z-1) == 1:
            return a
    return None


""" build random polynomials of a given degree and evalute in all field elemets.
stops when a polynomial has no roots.
""" 
def find_irreducible_polynomial(GFint,degree):
    ff_size = len(GFint.exptable)
    print ff_size
    while True:
        poly = Polynomial(GFint(random.randint(0,10)) for _ in range(degree+1))
        print 'testing {}'.format(poly)
        for v in range(ff_size+1):
            if poly.evaluate(GFint(v)) == 0:
                print '{} is a root'.format(v)
                break
        if v == ff_size:
            print poly
            return poly

            
def generate_exp_table(z,a):
    exptable = [a ** e % z for e in range(z)]
    return tuple(exptable)
    
def generate_log_table(z,a):
    exptable = [a ** e % z for e in range(z)]
    logtable = [None,] + [exptable.index(v) for v in range(1,z)]
    return tuple(logtable)
    
def int2poly(GFint,x):
    coef = []
    ff_size = len(GFint.exptable)
    while x > 0:
        coef.append(GFint(x % ff_size))
        x = x // ff_size
    return Polynomial(reversed(coef))
    
def poly2int(GFint,p):
    x = 0
    ff_size = len(GFint.exptable)
    for e,c in enumerate(reversed(p.coefficients)):
        x += int(c)*(ff_size ** e)
    return x
    
def factors(n):
    i = 2
    factors = []
    for i in range(2,n):
        if not n % i:
            factors.append(i)
    return factors   
 
def find_generator_element_extension(GFint,p):
    deg = p.degree()
    ff_size = len(GFint.exptable)
    fact = factors((ff_size ** deg -1))
    one = Polynomial((GFint(1),))
    for a in range(2,ff_size ** deg):
        poly = int2poly(GFint,a)
        print 'testing', a, poly
        pp = one
        for e in fact:
            pp = poly ** e
            pp = pp % p
            print 'power', e, pp
            if pp == one:
                print 'not generator since', pp, 'is 1'
                break
        if pp != one:
            print poly, pp
            return a
            
            
def generate_exp_table_extension(p,a,GFint):
    a_p = int2poly(GFint,a)
    pp = a_p
    deg = p.degree()
    ff_size = len(GFint.exptable)
    one = Polynomial((GFint(1),))
    exptable = [one,pp]
    while pp != one:
        pp = pp * a_p % p
        exptable.append(pp)
    return tuple(poly2int(GFint,pp) for pp in exptable)
    
def generate_log_table_extension(p,a,GFint):
    exptable = generate_exp_table_extension(p,a,GFint)
    logtable = [None,] + [exptable.index(v) for v in range(1,len(exptable))]
    return tuple(logtable)
