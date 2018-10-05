# Copyright (c) 2010 Andrew Brown <brownan@cs.duke.edu, brownan@gmail.com>
# See LICENSE.txt for license terms

class GFint(int):
    """Instances of this object are elements of the field GF(5)
    Instances are integers in the range 0 to 4
    and using 2 as the generator for the exponent table and log table.
    """
    # Maps integers to GF125int instances
    cache = {}
    # Exponent table for 2, a generator for GF(5)
    exptable = (1, 2, 4, 3, 1)

    # Logarithm table, base 2
    logtable = (None, 0, 1, 3, 2)

    def __new__(cls, value):
        # Check cache
        # Caching sacrifices a bit of speed for less memory usage. This way,
        # there are only a max of 256 instances of this class at any time.
        try:
            return GFint.cache[value]
        except KeyError:
            if value > 4 or value < 0:
                raise ValueError("Field elements of GF(5) are between 0 and 4. Cannot be %s" % value)

            newval = int.__new__(cls, value)
            GFint.cache[int(value)] = newval
            return newval

    def __add__(a, b):
        "Addition in GF(5) is done modulo 5"
        aa = int(a)
        bb = int(b)
        return GFint((aa + bb) % 5)
    def __sub__(self, other):
        return self + -other
    __radd__ = __add__
    def __rsub__(self, other):
        return self + -other
    def __neg__(self):
        return GFint((5 - int(self)) % 5)
    
    def __mul__(a, b):
        "Multiplication in GF(5)"
        if a == 0 or b == 0:
            return GFint(0)
        x = GFint.logtable[a]
        y = GFint.logtable[b]
        z = (x + y) % 4
        return GFint(GFint.exptable[z])
    __rmul__ = __mul__

    def __pow__(self, power):
        if isinstance(power, GFint):
            raise TypeError("Raising a Field element to another Field element is not defined. power must be a regular integer")
        x = GFint.logtable[self]
        z = (x * power) % 4
        return GFint(GFint.exptable[z])

    def inverse(self):
        e = GFint.logtable[self]
        return GFint(GFint.exptable[4 - e])

    def __div__(self, other):
        return self * GFint(other).inverse()
    def __rdiv__(self, other):
        return self.inverse() * other

    def __repr__(self):
        n = self.__class__.__name__
        return "%s(%r)" % (n, int(self))