# Copyright (c) 2010 Andrew Brown <brownan@cs.duke.edu, brownan@gmail.com>
# See LICENSE.txt for license terms

import ff_operations
from ff59 import GFint
from polynomial import Polynomial


def int2base59(x):
    assert x < 3481
    return (x//59,x%59)

def base59toint(x):
    assert len(x) == 2
    assert all(xx<59 for xx in x)
    return GFint(x[0]*59+x[1])


class GFint(int):
    """Instances of this object are elements of the field GF(59^2)
    Instances are integers in the range 0 to 3480
    This field is defined using the irreducable polynomial
    x^2 + 2x + 8
    and using 59 as the generator for the exponent table and log table.
    """
    p = 59
    n = 2
    alpha = 59
    poly = Polynomial((GFint(1),GFint(2),GFint(8)))
    # Maps integers to GF3481int instances
    cache = {}
    # Exponent table for 59, a generator for GF(3481)
    exptable = ff_operations.generate_exp_table_extension(poly,59,GFint)

    # Logarithm table, base 59
    logtable = ff_operations.generate_log_table_extension(poly,59,GFint)

    def __new__(cls, value):
        # Check cache
        # Caching sacrifices a bit of speed for less memory usage. This way,
        # there are only a max of 3481 instances of this class at any time.
        try:
            return GFint.cache[value]
        except KeyError:
            if value > 3480 or value < 0:
                raise ValueError("Field elements of GF(59^2) are between 0 and 3480. Cannot be %s" % value)

            newval = int.__new__(cls, value)
            GFint.cache[int(value)] = newval
            return newval

    def __add__(a, b):
        "Addition in GF(3481) is done as a 2 elements vector over GF(59)"
        a59 = int2base59(a)
        b59 = int2base59(b)
        c59 = [(aa+bb)%59 for aa,bb in zip(a59,b59)]
        return base59toint(c59)

    def __sub__(self, other):
        return self + -other
    __radd__ = __add__
    def __rsub__(self, other):
        return self + -other
    def __neg__(self):
        self59 = int2base59(self)
        res59 = tuple((59-v)%59 for v in self59)
        return base59toint(res59)
    
    def __mul__(a, b):
        "Multiplication in GF(59^2)"
        if a == 0 or b == 0:
            return GFint(0)
        x = GFint.logtable[a]
        y = GFint.logtable[b]
        z = (x + y) % 3480
        return GFint(GFint.exptable[z])
    __rmul__ = __mul__

    def __pow__(self, power):
        if isinstance(power, GFint):
            raise TypeError("Raising a Field element to another Field element is not defined. power must be a regular integer")
        x = GFint.logtable[self]
        z = (x * power) % 3480
        return GFint(GFint.exptable[z])

    def inverse(self):
        e = GFint.logtable[self]
        return GFint(GFint.exptable[3480 - e])

    def __div__(self, other):
        return self * GFint(other).inverse()
    def __rdiv__(self, other):
        return self.inverse() * other

    def __repr__(self):
        n = self.__class__.__name__
        return "%s(%r)" % (n, int(self))
        