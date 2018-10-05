# Copyright (c) 2010 Andrew Brown <brownan@cs.duke.edu, brownan@gmail.com>
# See LICENSE.txt for license terms

class GFint(int):
    """Instances of this object are elements of the field GF(7)
    Instances are integers in the range 0 to 6
    and using 3 as the generator for the exponent table and log table.
    """
    # Maps integers to GF125int instances
    cache = {}
    # Exponent table for 2, a generator for GF(7)
    exptable = (1, 3, 2, 6, 4, 5, 1)

    # Logarithm table, base 2
    logtable = (None, 0, 2, 1, 4, 5, 3)

    def __new__(cls, value):
        # Check cache
        # Caching sacrifices a bit of speed for less memory usage. This way,
        # there are only a max of 256 instances of this class at any time.
        try:
            return GFint.cache[value]
        except KeyError:
            if value > 6 or value < 0:
                raise ValueError("Field elements of GF(7) are between 0 and 6. Cannot be %s" % value)

            newval = int.__new__(cls, value)
            GFint.cache[int(value)] = newval
            return newval

    def __add__(a, b):
        "Addition in GF(7) is done modulo 5"
        aa = int(a)
        bb = int(b)
        return GFint((aa + bb) % 7)
    def __sub__(self, other):
        return self + -other
    __radd__ = __add__
    def __rsub__(self, other):
        return self + -other
    def __neg__(self):
        return GFint((7 - int(self)) % 7)
    
    def __mul__(a, b):
        "Multiplication in GF(7)"
        if a == 0 or b == 0:
            return GFint(0)
        x = GFint.logtable[a]
        y = GFint.logtable[b]
        z = (x + y) % 6
        return GFint(GFint.exptable[z])
    __rmul__ = __mul__

    def __pow__(self, power):
        if isinstance(power, GFint):
            raise TypeError("Raising a Field element to another Field element is not defined. power must be a regular integer")
        x = GFint.logtable[self]
        z = (x * power) % 6
        return GFint(GFint.exptable[z])

    def inverse(self):
        e = GFint.logtable[self]
        return GFint(GFint.exptable[6 - e])

    def __div__(self, other):
        return self * GFint(other).inverse()
    def __rdiv__(self, other):
        return self.inverse() * other

    def __repr__(self):
        n = self.__class__.__name__
        return "%s(%r)" % (n, int(self))