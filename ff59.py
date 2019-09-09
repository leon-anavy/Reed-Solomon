# Copyright (c) 2010 Andrew Brown <brownan@cs.duke.edu, brownan@gmail.com>
# See LICENSE.txt for license terms 

class GFint(int):
    """Instances of this object are elements of the field GF(59)
    Instances are integers in the range 0 to 58
    and using 2 as the generator for the exponent table and log table.
    """
    # Maps integers to GF125int instances
    cache = {}
    # Exponent table for 2, a generator for GF(59)
    exptable = (1, 2, 4, 8, 16, 32, 5, 10, 20, 40, 21, 42, 25, 50, 41, 23, 46, 33, 7, 14, 28, 56,
               53, 47, 35, 11, 22, 44, 29, 58, 57, 55, 51, 43, 27, 54, 49, 39, 19, 38, 17, 34,
               9, 18, 36, 13, 26, 52, 45, 31, 3, 6, 12, 24, 48, 37, 15, 30, 1)

    # Logarithm table, base 2
    logtable = (None, 0, 1, 50, 2, 6, 51, 18, 3, 42, 7, 25, 52, 45, 19, 56, 4, 40, 43, 38, 8, 10, 26, 15,
                53, 12, 46, 34, 20, 28, 57, 49, 5, 17, 41, 24, 44, 55, 39, 37, 9, 14, 11, 33, 27, 48,
                16, 23, 54, 36, 13, 32, 47, 22, 35, 31, 21, 30, 29)

    def __new__(cls, value):
        # Check cache
        # Caching sacrifices a bit of speed for less memory usage. This way,
        # there are only a max of 256 instances of this class at any time.
        try:
            return GFint.cache[value]
        except KeyError:
            if value > 58 or value < 0:
                raise ValueError("Field elements of GF(59) are between 0 and 58. Cannot be %s" % value)

            newval = int.__new__(cls, value)
            GFint.cache[int(value)] = newval
            return newval

    def __add__(a, b):
        "Addition in GF(59) is done modulo 59"
        aa = int(a)
        bb = int(b)
        return GFint((aa + bb) % 59)
    def __sub__(self, other):
        return self + -other
    __radd__ = __add__
    def __rsub__(self, other):
        return self + -other
    def __neg__(self):
        return GFint((59 - int(self)) % 59)
    
    def __mul__(a, b):
        "Multiplication in GF(59)"
        if a == 0 or b == 0:
            return GFint(0)
        x = GFint.logtable[a]
        y = GFint.logtable[b]
        z = (x + y) % 58
        return GFint(GFint.exptable[z])
    __rmul__ = __mul__

    def __pow__(self, power):
        if isinstance(power, GFint):
            raise TypeError("Raising a Field element to another Field element is not defined. power must be a regular integer")
        x = GFint.logtable[self]
        z = (x * power) % 58
        return GFint(GFint.exptable[z])

    def inverse(self):
        e = GFint.logtable[self]
        return GFint(GFint.exptable[58 - e])

    def __div__(self, other):
        return self * GFint(other).inverse()
    def __rdiv__(self, other):
        return self.inverse() * other

    def __repr__(self):
        n = self.__class__.__name__
        return "%s(%r)" % (n, int(self))