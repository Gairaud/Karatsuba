"""
AUTORES:
1) Kevin Flores G             
2) Philippe Gairaud                     
"""

from functools import total_ordering
from abc import ABC, abstractmethod

Default_base = 10
MAX_SIZE = 16

@total_ordering
class AbstractNum:

    @abstractmethod
    def __add__(self, other) : pass

    @abstractmethod
    def __mul__(self, other) : pass

    @abstractmethod
    def __pow__(self,other): pass

    @abstractmethod
    def multbyOneDigit(self,digits): pass

    @abstractmethod
    def __floordiv__(self, other) : pass

    @abstractmethod
    def __sub__(self, other) : pass

    @abstractmethod
    def __eq__(self,other) : pass

    @abstractmethod
    def __lt__(self, other) : pass

    @abstractmethod
    def __invert__(self) : pass 

    def operateValidator(self,other):
        """
        Raise a exception if the user tries to operate a Num or Knum with
        others data types of data

        -Example
            Num + int
            Num + Knum
        """
        if(type(self)!=type(other)):
            raise Exception(f"Can't operate {self.__class__.__name__} with {other.__class__.__name__}")

    def creationBase(self,digits,base):
        """
        Raise a exception if a number in the digits list is equal or greater
        than the creation base

        -Example
            45 in base 4
            49 in base 8
        """
        for x in str(digits):
            if int(x) >= base:
                raise Exception(f"Can't create a number with a digit of the same value or greater than base {base}")

class Num(AbstractNum):

    def __init__(self, digits = 0, b = Default_base, is_comple = False):
        """
        Initialize a Num object with digits, base and complement
        The Num with digits = 345 has the next form 
        --> [0,...,0,3,4,5] 
        """
        self.base = b
        self.is_complement = is_comple
        self.creationBase(digits,self.base)
        numberList = [int(x) for x in str(digits)]
        if len(numberList) == 0: numberList = [0]
        self.numDigits = len(numberList)
        if self.numDigits > MAX_SIZE:
            raise Exception("Overflow")
        else: 
            self.num = [0] * MAX_SIZE
        for y in range(MAX_SIZE - self.numDigits, MAX_SIZE):
            self.num[y] = numberList.pop(0)
    
    def __str__(self):
        x = ""
        if self.is_complement : y = ~self
        else:  y = self
        for i in range(len(y)):
            x += str(y[i])
        if self.is_complement: return f"({type(self).__name__})(base = {self.base})(-{x})"
        return f"({type(self).__name__})(base = {self.base})({x})"
        
    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return self.numDigits
        
    def __getitem__(self, key):
        if key > self.numDigits:
            raise Exception("Overflow")
        return self.num[MAX_SIZE - (len(self) - key)]

    def __add__(self, other):
        """Returns the sum of two Nums 
         -Example

        + [1,2,3]
          [1,2,3]
        _________
          [2,4,6]
        """ 
        Num.operateValidator(self,other)
        if self.base != other.base:
            raise Exception("Different Bases")
        else:
            # Verifying sums -> "~Num + Num", "Num + ~Num", "~Num + ~Num"
            if self.is_complement and other.is_complement: return ~(~self + ~other)
            elif self.is_complement and not other.is_complement:
                if ~self > other: return ~(~other - self)
            elif not self.is_complement and other.is_complement:
                if self < ~other: return ~(~self - other)
            #-------------------------------------------------------------
            result, result_num = [], 0
            llevo = False
            for x in range(MAX_SIZE-1, -1, -1):
                sum = self.num[x] + other.num[x]
                if llevo: sum += 1
                if sum >= self.base:
                    result.append(sum - self.base)
                    llevo = True
                else:
                    result.append(sum)
                    llevo = False
            for i in range(len(result)): result_num += result[i]*10**i
            return type(self)(result_num, self.base)

    def __mul__(self, other):
        """Returns the multiplication of two Nums 
         -Example

        * [1,3]
          [4,5]
        _________
        + [6,5]
        [5,2]
        _________
        [5,8,5]
        """ 
        Num.operateValidator(self,other)
        if self.base != other.base:
            raise Exception("Different Bases")
        else:
            # Verifying multiplications -> "~Num * Num", "Num * ~Num", "~Num * ~Num"
            if self.is_complement and not other.is_complement: return ~(~self*other)
            elif not self.is_complement and other.is_complement: return ~(self*~other)
            elif self.is_complement and other.is_complement: return ~self*~other
            #-----------------------------------------------------------------------
            result = []
            llevo = False
            total = type(self)(digits = 0, b = self.base)
            zeros = [0]
            c, carry = 0, 0
            for x in range(MAX_SIZE-1, -1+c, -1):
                result = []
                result.extend(zeros*c)
                for y in range (MAX_SIZE-1, -1+c, -1):
                    sum = self.num[y] * other.num[x]
                    if llevo: sum += carry 
                    if sum >= self.base:
                        result.append(sum - (self.base * (sum//self.base)))
                        llevo = True
                        carry = sum // self.base
                    else:
                        result.append(sum)
                        llevo = False
                c +=1
                result = result[::-1]
                total = total +  type(self)("".join(str(i) for i in result), self.base)
            return total

    def __floordiv__(self, other):
        """Returns the division of two Nums 
         -Example

        [1,0] // [2]
        ______________

          [1,0]  | [2]
                 |______
        -[2]*[5] | [5]
        _________|
           [0]   |
        _________
        return [5]
        """ 
        Num.operateValidator(self,other)
        if self.base != other.base:
            raise Exception("Different Bases")
        else:
            # Verifying divisions -> "~Num // Num", "Num // ~Num", "~Num // ~Num"
            if self.is_complement and not other.is_complement: return ~(~self//other)
            elif not self.is_complement and other.is_complement: return ~(self//~other)
            elif self.is_complement and other.is_complement: return ~self//~other
            #---------------------------------------------------------------------
            result, num, enter = [0], '', False
            for x in range(MAX_SIZE - self.numDigits, MAX_SIZE):
                num += str(self.num[x])
                aux_1 = type(self)(digits = num, b = self.base)
                if  aux_1 >= other:
                    if not enter: result = []
                    enter = True
                    while (x < MAX_SIZE):
                        multiply = 1
                        aux_2 = type(other)(digits = multiply, b = other.base) * other 
                        while aux_2 <= aux_1: 
                            multiply += 1
                            aux_2 = type(self)(digits = multiply, b = self.base) * other  
                        result.append(multiply)
                        aux_3 = type(self)("".join(str(i) for i in result), self.base) * other
                        while aux_2 > aux_1 or aux_3 > self:
                            multiply -= 1
                            result[len(result)-1] = multiply
                            aux_2 = type(self)(digits = multiply, b = self.base) * other
                            aux_3 = type(self)("".join(str(i) for i in result), self.base) * other
                        x += 1
                        if x < MAX_SIZE : 
                            aux_1 = aux_1 - aux_2
                            aux_1 = aux_1 << 1
                            aux_1 = aux_1 + type(self)(digits=self.num[x], b = self.base)
                if enter: break         
            return  type(self)("".join(str(i) for i in result), self.base) 
        
    def __sub__(self, other):
        """Returns the substarction of two Nums 
         -Example          -Complement example

        - [1,2,3]             -[1,2,3]
            [2,3]              [2,0,0]
        _________            _________
          [1,0,0]           [..,9,2,3]
        """ 
        Num.operateValidator(self,other)
        if self.base != other.base:
            raise Exception("Different Bases")
        else:
            result = self + ~other
            if self < other: result.is_complement = True
            return result
    
    def __pow__(self, other):
        """
        Raise a Num to the powe of other Num
        -Example
            [1,2]**[2]
        """
        result = self
        exponent = int("".join(str(i) for i in other.num))
        for i in  range (exponent-1):
            result = result*self
        return result

    def multbyOneDigit(self,digit):
        """
        Multiply a Num by a int
        -Example
        2* [2,3]
        """
        result = self
        for i in  range (digit-1):
            result = result+self
        return result

    def __invert__(self):   
        x = [ self.base - 1 - x for x in self.num ]
        result = type(self)("".join(str(i) for i in x), self.base) + type(self)(1, self.base)
        result.is_complement = False if self.is_complement else True
        return result

    def __eq__(self, other):
        Num.operateValidator(self,other)
        if self.base != other.base:
            raise Exception("Different Bases")
        for x in range(MAX_SIZE-1,-1,-1):
            if self.num[x] != other.num[x] : return False
        return True

    def __lt__(self, other):
        Num.operateValidator(self,other)
        if self.base != other.base:
            raise Exception("Different Bases")
        if (other.is_complement and not self.is_complement) or self == other: return False
        if self.is_complement and not other.is_complement: return True
        else:
            if len(self) > len(other): return False
            elif len(self) == len(other):
                k, y = 0,0
                for x in range(self.numDigits -1, -1, -1):
                    k += self.num[MAX_SIZE - x - 1]*10**x
                    y += other.num[MAX_SIZE - x - 1]*10**x
                    if k > y: return False
        return True

    def __lshift__(self, position):
        # using multiplication
        # return self * type(self)(digits = 10**position, b =self.base)
        # To avoid calling the multiplication
        self.num.extend([0]*position)
        for x in range(position) :  self.num.pop(0) 
        self.numDigits += position
        return self

    def __rshift__(self, position):
        # using division
        # return self // type(self)(digits = 10**position, b = self.base)
        # To avoid calling the division
        for x in range(position):  
            self.num.pop()
            self.num.insert(0,0) 
        self.numDigits -= position
        return self

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
            # Verifying multiplications -> "~Knum * Knum", "Knum * ~Num", "~Knum * ~Knum"
            if self.is_complement and not other.is_complement: return ~(~self*other)
            elif not self.is_complement and other.is_complement: return ~(self*~other)
            elif self.is_complement and other.is_complement: return ~self*~other

            # CALCULADING N/2 = NUMER OF DIGITS/2
            Lself = len(self)
            Lother = len(other)
            n = Lself // 2 + Lself % 2 if Lself >= Lother else Lother // 2 + Lother % 2

            # MIDDLE OF THE NUMBERS
            if Lself == Lother:
                mid_self = MAX_SIZE - Lself + n
                mid_other = MAX_SIZE - Lother + n
            elif Lself > Lother:
                mid_self = MAX_SIZE - Lself + (Lself - n) 
                mid_other = MAX_SIZE - Lother
            else: 
                mid_self = MAX_SIZE - Lself 
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

if __name__=="__main__":
    
    i = Knum(12,5)
    j = Knum("310",5)
    print(i*j)