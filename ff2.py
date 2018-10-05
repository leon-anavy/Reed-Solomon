# Copyright (c) 2010 Andrew Brown <brownan@cs.duke.edu, brownan@gmail.com>
# See LICENSE.txt for license terms

class GFint(int):
    """Instances of this object are elements of the field GF(2)
    Instances are integers in the range 0 to 1
    and using 2 as the generator for the exponent table and log table.
    """
    # Maps integers to GF125int instances
    def __new__(cls, value):
        # Check cache
        # Caching sacrifices a bit of speed for less memory usage. This way,
        # there are only a max of 256 instances of this class at any time.
        if value > 4 or value < 0:
            raise ValueError("Field elements of GF(5) are between 0 and 4. Cannot be %s" % value)

        newval = int.__new__(cls, value)
        return newval

    def __add__(a, b):
        "Addition in GF(2) is xor"
        return GFint(a ^ b)
    __sub__ = __add__
    __radd__ = __add__
    __rsub__ = __add__
    def __neg__(self):
        return self
    
    def __mul__(a, b):
        "Multiplication in GF(2)"
        return GFint(a & b)
    __rmul__ = __mul__

    def __pow__(self, power):
        if isinstance(power, GFint):
            raise TypeError("Raising a Field element to another Field element is not defined. power must be a regular integer")
        if power < 0:
            raise ValueError("no negative power supported")
        if power > 0:
            return self
        return GFint(1)

    def inverse(self):
        if self:
            return self
        return None

    def __div__(self, other):
        return self * GFint(other).inverse()
    def __rdiv__(self, other):
        return self.inverse() * GFint(other)

    def __repr__(self):
        n = self.__class__.__name__
        return "%s(%r)" % (n, int(self))