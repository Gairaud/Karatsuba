"""
Authors:
1) Kevin Flores G             
2) Philippe Gairaud     

KnumClass
"""
from NaturalNumber import *

class Knum(Num):
    def __mul__(self, other):
        """Returns the multiplication of two Knums 
         -Example

        * [1,3]
          [4,5]
        _________

        n = len(Longer Num)//2 = 2//2 = 1
        a = [1], b = [3], c = [4], d = [5]

        ac = a * c = [1]*[4] = [4]
        bd = b * d = [3]*[5] = [1,5]
        ad + bc = ( a+b )*( c+d ) - ac - bd
                = ( [1]+[3] )*( [4]+[5] ) - [4] - [1,5]
                = [1,7]
        
        (ac << 2*n) + (ad + bc << n) + bd
        = [4,0,0] + [1,7,0] + [1,5]
        ___________________________
                [5,8,5]
        """ 
        Knum.operateValidator(self, other)
        # BASE CASE
        if len(self) == 1 and len(other) == 1: 
            return super().__mul__(other)
        else:
            # Verifying multiplications -> "~Knum * Knum", "Knum * ~Knum", "~Knum * ~Knum"
            if self.is_complement and not other.is_complement: return ~(~self*other)
            elif not self.is_complement and other.is_complement: return ~(self*~other)
            elif self.is_complement and other.is_complement: return ~self*~other

            # CALCULADING N/2 = NUMER OF DIGITS/2
            Lself = len(self)
            Lother = len(other)
            n = Lself // 2 + Lself % 2 if Lself >= Lother else Lother // 2 + Lother % 2

            # MIDDLE OF THE NUMBERS
            mid_self = MAX_SIZE - Lself + (Lself - n)
            mid_other = MAX_SIZE - Lother + (Lother - n)  
                
            # CREATING NEW KNUMBER's FROM THE PREVIOUS KNUMBER'S 
            a = type(self)("".join(str(i) for i in self.num[MAX_SIZE-Lself:mid_self]), self.base)
            b = type(self)("".join(str(i) for i in self.num[mid_self:]), self.base)
            c = type(other)("".join(str(i) for i in other.num[MAX_SIZE-Lother:mid_other]), other.base)
            d = type(other)("".join(str(i) for i in other.num[mid_other:]), other.base)

            # RECURSIVE CALL's (3 MULTIPLICATION's INSTEAD OF 4)
            ac = a*c
            bd = b*d
            ad_bc = (a+b)*(c+d) - ac - bd

        # END
        return (ac << 2*n) + (ad_bc << n) + bd