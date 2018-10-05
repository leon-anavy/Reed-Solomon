# Copyright (c) 2010 Andrew Brown <brownan@cs.duke.edu, brownan@gmail.com>
# See LICENSE.txt for license terms

def int2base7(x):
    assert x < 343
    return (x//49,(x%49)//7,(x%49)%7)

def base5toint(x):
    assert len(x) == 3
    assert all(xx<7 for xx in x)
    return GFint(x[0]*49+x[1]*7+x[2])

class GFint(int):
    """Instances of this object are elements of the field GF(343)
    Instances are integers in the range 0 to 342
    This field is defined using the irreducable polynomial
    3x^3 + 6x^2 + 6x + 2
    and using 8 as the generator for the exponent table and log table.
    """
    p = 7
    n = 3
    alpha = 8
    # Maps integers to GF343int instances
    cache = {}

    # Exponent table for 8, a generator for GF(343)
    exptable = (
         1, 8, 64, 61, 30, 240, 102, 250, 116, 19, 103, 258, 180, 73, 126, 99, 275, 316, 242, 118, 28, 224, 23, 184, 105,
         323, 249, 108, 298, 91, 277, 332, 321, 226, 39, 263, 220, 334, 330, 305, 98, 267, 252, 188, 137, 187, 129, 123,
         75, 142, 227, 47, 327, 274, 308, 178, 57, 5, 40, 271, 284, 45, 311, 153, 200, 174, 25, 151, 233, 95, 253, 189,
         152, 241, 110, 314, 170, 42, 336, 10, 80, 182, 145, 202, 183, 104, 259, 244, 127, 107, 339, 34, 223, 302, 130,
         131, 139, 147, 208, 231, 79, 181, 81, 190, 160, 256, 164, 337, 18, 144, 243, 119, 92, 285, 4, 32, 207, 230, 15,
         120, 51, 300, 58, 13, 55, 325, 265, 236, 63, 53, 309, 186, 121, 59, 14, 112, 36, 288, 77, 165, 296, 82, 149,
         217, 310, 194, 185, 113, 44, 303, 138, 195, 193, 177, 49, 333, 322, 290, 93, 293, 68, 86, 237, 71, 117, 27,
         167, 312, 154, 264, 228, 6, 48, 335, 338, 26, 159, 248, 100, 283, 37, 247, 141, 219, 326, 266, 251, 124, 83,
         157, 281, 21, 168, 33, 215, 287, 76, 101, 291, 52, 301, 122, 67, 78, 173, 17, 136, 179, 65, 69, 94, 245, 132,
         140, 211, 262, 212, 270, 276, 324, 257, 172, 9, 72, 125, 84, 221, 342, 2, 16, 128, 115, 11, 88, 197, 150, 225,
         31, 199, 166, 304, 146, 203, 198, 158, 289, 85, 229, 7, 56, 46, 319, 210, 254, 148, 216, 246, 133, 155, 272,
         292, 60, 22, 176, 97, 269, 268, 260, 196, 191, 161, 320, 218, 318, 209, 239, 143, 235, 62, 38, 255, 156, 273,
         307, 114, 3, 24, 192, 169, 41, 279, 299, 50, 341, 43, 295, 74, 134, 163, 329, 297, 90, 213, 278, 340, 35, 280,
         20, 111, 315, 234, 54, 317, 201, 175, 89, 205, 214, 286, 12, 96, 261, 204, 206, 222, 294, 66, 70, 109, 306,
         106, 331, 313, 162, 328, 282, 29, 232, 87, 238, 135, 171, 1)

    # Logarithm table, base 5
    logtable = (
         None, 0, 228, 285, 114, 57, 171, 248, 1, 222, 79, 232, 319, 123, 134, 118, 229, 205, 108, 9, 307, 191, 262, 22,
         286, 66, 175, 165, 20, 336, 4, 237, 115, 193, 91, 305, 136, 180, 279, 34, 58, 289, 77, 294, 148, 61, 250, 51,
         172, 154, 292, 120, 199, 129, 311, 124, 249, 56, 122, 133, 261, 3, 278, 128, 2, 208, 326, 202, 160, 209, 327,
         163, 223, 13, 296, 48, 196, 138, 203, 100, 80, 102, 141, 188, 225, 246, 161, 338, 233, 315, 301, 29, 112, 158,
         210, 69, 320, 264, 40, 15, 178, 197, 6, 10, 85, 24, 330, 89, 27, 328, 74, 308, 135, 147, 284, 231, 8, 164, 19,
         111, 119, 132, 201, 47, 187, 224, 14, 88, 230, 46, 94, 95, 212, 257, 297, 340, 206, 44, 150, 96, 213, 182, 49,
         276, 109, 82, 241, 97, 254, 142, 235, 67, 72, 63, 168, 258, 281, 189, 244, 176, 104, 270, 333, 298, 106, 139,
         239, 166, 192, 288, 76, 341, 221, 204, 65, 314, 263, 153, 55, 207, 12, 101, 81, 84, 23, 146, 131, 45, 43, 71,
         103, 269, 287, 152, 145, 151, 268, 234, 243, 238, 64, 313, 83, 242, 322, 316, 323, 116, 98, 274, 252, 214, 216,
         302, 317, 194, 255, 143, 272, 183, 36, 226, 324, 92, 21, 236, 33, 50, 170, 247, 117, 99, 337, 68, 310, 277,
         127, 162, 339, 275, 5, 73, 18, 110, 87, 211, 256, 181, 177, 26, 7, 186, 42, 70, 253, 280, 105, 220, 11, 86,
         267, 321, 215, 35, 169, 126, 185, 41, 266, 265, 217, 59, 259, 282, 53, 16, 218, 30, 303, 290, 306, 190, 335,
         179, 60, 113, 318, 195, 137, 245, 157, 198, 260, 159, 325, 295, 140, 300, 28, 291, 121, 200, 93, 149, 240, 39,
         329, 283, 54, 130, 144, 62, 167, 332, 75, 309, 17, 312, 273, 251, 271, 32, 156, 25, 219, 125, 184, 52, 334,
         299, 38, 331, 31, 155, 37, 173, 78, 107, 174, 90, 304, 293, 227)

    def __new__(cls, value):
        # Check cache
        # Caching sacrifices a bit of speed for less memory usage. This way,
        # there are only a max of 256 instances of this class at any time.
        try:
            return GFint.cache[value]
        except KeyError:
            if value > 342 or value < 0:
                raise ValueError("Field elements of GF(343) are between 0 and 342. Cannot be %s" % value)

            newval = int.__new__(cls, value)
            GFint.cache[int(value)] = newval
            return newval

    def __add__(a, b):
        "Addition in GF(343) is done as a 3 elements vector over GF(7)"
        a7 = int2base7(a)
        b7 = int2base7(b)
        c7 = [(aa+bb)%7 for aa,bb in zip(a7,b7)]
        return base5toint(c7)

    def __sub__(self, other):
        return self + -other
    __radd__ = __add__
    def __rsub__(self, other):
        return self + -other
    def __neg__(self):
        self7 = int2base7(self)
        res7 = tuple((7-v)%7 for v in self7)
        return base5toint(res7)
    
    def __mul__(a, b):
        "Multiplication in GF(343)"
        if a == 0 or b == 0:
            return GFint(0)
        x = GFint.logtable[a]
        y = GFint.logtable[b]
        z = (x + y) % 342
        return GFint(GFint.exptable[z])
    __rmul__ = __mul__

    def __pow__(self, power):
        if isinstance(power, GFint):
            raise TypeError("Raising a Field element to another Field element is not defined. power must be a regular integer")
        x = GFint.logtable[self]
        z = (x * power) % 342
        return GFint(GFint.exptable[z])

    def inverse(self):
        e = GFint.logtable[self]
        return GFint(GFint.exptable[342 - e])

    def __div__(self, other):
        return self * GFint(other).inverse()
    def __rdiv__(self, other):
        return self.inverse() * other

    def __repr__(self):
        n = self.__class__.__name__
        return "%s(%r)" % (n, int(self))