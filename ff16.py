# Copyright (c) 2010 Andrew Brown <brownan@cs.duke.edu, brownan@gmail.com>
# See LICENSE.txt for license terms

def int2base2(x):
    assert x < 16
    return [(x % 2 ** (4 - i)) // 2 ** (3 - i) for i in range(4)]

def base2toint(x):
    assert len(x) == 4
    assert all(xx<2 for xx in x)
    return GFint(sum(xx*(2**(3-i)) for i,xx in enumerate(x)))


class GFint(int):
    """Instances of this object are elements of the field GF(2^4)
    Instances are integers in the range 0 to 15
    This field is defined using the irreducable polynomial
    x^4 + x^3 + x^2 + x + 1
    and using 3 as the generator for the exponent table and log table.
    """
    p = 2
    n = 4
    alpha = 3
    # Maps integers to GF16int instances
    cache = {}
    # Exponent table for 3, a generator for GF(16)
    exptable = (1, 3, 5, 15, 14, 13, 8, 7, 9, 4, 12, 11, 2, 6, 10, 1)
    # Logarithm table, base 3
    logtable = (None, 0, 12, 1, 9, 2, 13, 7, 6, 8, 14, 11, 10, 5, 4, 3)

    def __new__(cls, value):
        # Check cache
        # Caching sacrifices a bit of speed for less memory usage. This way,
        # there are only a max of 16 instances of this class at any time.
        try:
            return GFint.cache[value]
        except KeyError:
            if value > 15 or value < 0:
                raise ValueError("Field elements of GF(2^4) are between 0 and 15. Cannot be %s" % value)

            newval = int.__new__(cls, value)
            GFint.cache[int(value)] = newval
            return newval

    def __add__(a, b):
        "Addition in GF(125) is done as a 3 elements vector over GF(5)"
        a2 = int2base2(a)
        b2 = int2base2(b)
        c2 = [(aa+bb)%2 for aa,bb in zip(a2,b2)]
        return base2toint(c2)

    __sub__ = __add__
    __radd__ = __add__
    __rsub__ = __add__
    def __neg__(self):
        return self
    
    def __mul__(a, b):
        "Multiplication in GF(2^6)"
        if a == 0 or b == 0:
            return GFint(0)
        x = GFint.logtable[a]
        y = GFint.logtable[b]
        z = (x + y) % 15
        return GFint(GFint.exptable[z])
    __rmul__ = __mul__

    def __pow__(self, power):
        if isinstance(power, GFint):
            raise TypeError("Raising a Field element to another Field element is not defined. power must be a regular integer")
        x = GFint.logtable[self]
        z = (x * power) % 15
        return GFint(GFint.exptable[z])

    def inverse(self):
        e = GFint.logtable[self]
        return GFint(GFint.exptable[15 - e])

    def __div__(self, other):
        return self * GFint(other).inverse()
    def __rdiv__(self, other):
        return self.inverse() * other

    def __repr__(self):
        n = self.__class__.__name__
        return "%s(%r)" % (n, int(self))
