# Copyright (c) 2010 Andrew Brown <brownan@cs.duke.edu, brownan@gmail.com>
# See LICENSE.txt for license terms

def int2base2(x):
    assert x < 64
    return [(x % 2 ** (6 - i)) // 2 ** (5 - i) for i in range(6)]

def base2toint(x):
    assert len(x) == 6
    assert all(xx<2 for xx in x)
    return GFint(sum(xx*(2**(5-i)) for i,xx in enumerate(x)))


class GFint(int):
    """Instances of this object are elements of the field GF(2^6)
    Instances are integers in the range 0 to 63
    This field is defined using the irreducable polynomial
    x^6 + x^5 + x^3 + x^2 + 1
    and using 2 as the generator for the exponent table and log table.
    """
    p = 2
    n = 6
    alpha = 2

    # Maps integers to GF64int instances
    cache = {}
    # Exponent table for 2, a generator for GF(64)
    exptable = (
    1, 2, 4, 8, 16, 32, 45, 55, 3, 6, 12, 24, 48, 13, 26, 52, 5, 10, 20, 40, 61, 23, 46, 49, 15, 30, 60, 21, 42, 57, 31,
    62, 17, 34, 41, 63, 19, 38, 33, 47, 51, 11, 22, 44, 53, 7, 14, 28, 56, 29, 58, 25, 50, 9, 18, 36, 37, 39, 35, 43,
    59, 27, 54, 1)
    # Logarithm table, base 2
    logtable = (
    None, 0, 1, 8, 2, 16, 9, 45, 3, 53, 17, 41, 10, 13, 46, 24, 4, 32, 54, 36, 18, 27, 42, 21, 11, 51, 14, 61, 47, 49,
    25, 30, 5, 38, 33, 58, 55, 56, 37, 57, 19, 34, 28, 59, 43, 6, 22, 39, 12, 23, 52, 40, 15, 44, 62, 7, 48, 29, 50, 60,
    26, 20, 31, 35)

    def __new__(cls, value):
        # Check cache
        # Caching sacrifices a bit of speed for less memory usage. This way,
        # there are only a max of 64 instances of this class at any time.
        try:
            return GFint.cache[value]
        except KeyError:
            if value > 63 or value < 0:
                raise ValueError("Field elements of GF(2^6) are between 0 and 63. Cannot be %s" % value)

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
        z = (x + y) % 63
        return GFint(GFint.exptable[z])
    __rmul__ = __mul__

    def __pow__(self, power):
        if isinstance(power, GFint):
            raise TypeError("Raising a Field element to another Field element is not defined. power must be a regular integer")
        x = GFint.logtable[self]
        z = (x * power) % 63
        return GFint(GFint.exptable[z])

    def inverse(self):
        e = GFint.logtable[self]
        return GFint(GFint.exptable[63 - e])

    def __div__(self, other):
        return self * GFint(other).inverse()
    def __rdiv__(self, other):
        return self.inverse() * other

    def __repr__(self):
        n = self.__class__.__name__
        return "%s(%r)" % (n, int(self))
