# Copyright (c) 2010 Andrew Brown <brownan@cs.duke.edu, brownan@gmail.com>
# See LICENSE.txt for license terms

def int2base5(x):
    assert x < 125
    return (x//25,(x%25)//5,(x%25)%5)

def base5toint(x):
    assert len(x) == 3
    assert all(xx<5 for xx in x)
    return GFint(x[0]*25+x[1]*5+x[2])

class GFint(int):
    """Instances of this object are elements of the field GF(125)
    Instances are integers in the range 0 to 124
    This field is defined using the irreducable polynomial
    x^3 + 2x^2 + 3
    and using 5 as the generator for the exponent table and log table.
    """
    p = 5
    n = 3
    alpha = 5
    # Maps integers to GF125int instances
    cache = {}

    # Exponent table for 5, a generator for GF(125)
    exptable = (
    1, 5, 25, 77, 111, 108, 93, 66, 109, 98, 91, 56, 59, 74, 24, 120, 28, 92, 61, 84, 21, 105, 78, 116, 8, 40, 27, 87,
    36, 7, 35, 2, 10, 50, 29, 97, 86, 31, 107, 88, 41, 32, 112, 113, 118, 18, 90, 51, 34, 122, 38, 17, 85, 26, 82, 11,
    55, 54, 49, 72, 14, 70, 4, 20, 100, 53, 44, 47, 62, 89, 46, 57, 64, 99, 96, 81, 6, 30, 102, 63, 94, 71, 9, 45, 52,
    39, 22, 110, 103, 68, 119, 23, 115, 3, 15, 75, 101, 58, 69, 124, 48, 67, 114, 123, 43, 42, 37, 12, 60, 79, 121, 33,
    117, 13, 65, 104, 73, 19, 95, 76, 106, 83, 16, 80, 1)

    # Logarithm table, base 5
    logtable = (
    None, 0, 31, 93, 62, 1, 76, 29, 24, 82, 32, 55, 107, 113, 60, 94, 122, 51, 45, 117, 63, 20, 86, 91, 14, 2, 53, 26,
    16, 34, 77, 37, 41, 111, 48, 30, 28, 106, 50, 85, 25, 40, 105, 104, 66, 83, 70, 67, 100, 58, 33, 47, 84, 65, 57, 56,
    11, 71, 97, 12, 108, 18, 68, 79, 72, 114, 7, 101, 89, 98, 61, 81, 59, 116, 13, 95, 119, 3, 22, 109, 123, 75, 54,
    121, 19, 52, 36, 27, 39, 69, 46, 10, 17, 6, 80, 118, 74, 35, 9, 73, 64, 96, 78, 88, 115, 21, 120, 38, 5, 8, 87, 4,
    42, 43, 102, 92, 23, 112, 44, 90, 15, 110, 49, 103, 99)

    def __new__(cls, value):
        # Check cache
        # Caching sacrifices a bit of speed for less memory usage. This way,
        # there are only a max of 256 instances of this class at any time.
        try:
            return GFint.cache[value]
        except KeyError:
            if value > 124 or value < 0:
                raise ValueError("Field elements of GF(125) are between 0 and 124. Cannot be %s" % value)

            newval = int.__new__(cls, value)
            GFint.cache[int(value)] = newval
            return newval

    def __add__(a, b):
        "Addition in GF(125) is done as a 3 elements vector over GF(5)"
        a5 = int2base5(a)
        b5 = int2base5(b)
        c5 = [(aa+bb)%5 for aa,bb in zip(a5,b5)]
        return base5toint(c5)

    def __sub__(self, other):
        return self + -other
    __radd__ = __add__
    def __rsub__(self, other):
        return self + -other
    def __neg__(self):
        self5 = int2base5(self)
        res5 = tuple((5-v)%5 for v in self5)
        return base5toint(res5)
    
    def __mul__(a, b):
        "Multiplication in GF(5)"
        if a == 0 or b == 0:
            return GFint(0)
        x = GFint.logtable[a]
        y = GFint.logtable[b]
        z = (x + y) % 124
        return GFint(GFint.exptable[z])
    __rmul__ = __mul__

    def __pow__(self, power):
        if isinstance(power, GFint):
            raise TypeError("Raising a Field element to another Field element is not defined. power must be a regular integer")
        x = GFint.logtable[self]
        z = (x * power) % 124
        return GFint(GFint.exptable[z])

    def inverse(self):
        e = GFint.logtable[self]
        return GFint(GFint.exptable[124 - e])

    def __div__(self, other):
        return self * GFint(other).inverse()
    def __rdiv__(self, other):
        return self.inverse() * other

    def __repr__(self):
        n = self.__class__.__name__
        return "%s(%r)" % (n, int(self))