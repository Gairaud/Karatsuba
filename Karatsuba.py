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
        if(type(self)!=type(other)):
            raise Exception(f"Can't operate {self.__class__.__name__} with {other.__class__.__name__}")
    def creationBase(self,digits,base):
        for x in str(digits):
            if int(x) >= base:
                raise Exception(f"Can't create a number with a digit of the same value or greater than base {base}")
class Num(AbstractNum):
    def __init__(self, digits = 0, b = Default_base, is_comple = False):
        self.base = b
        self.is_complement = is_comple
        self.creationBase(digits,self.base)
        numberList = [int(x) for x in str(digits)]
        if len(numberList) == 0: numberList = [1]
        self.numDigits = len(numberList)
        if self.numDigits > MAX_SIZE:
            raise Exception("Overflow")
        else: 
            self.num = [0] * MAX_SIZE
        for y in range(MAX_SIZE - self.numDigits, MAX_SIZE):
            self.num[y] = numberList.pop(0)
    
    def __str__(self):
        x = ""
        for i in range(MAX_SIZE-len(self), MAX_SIZE):
            x += str(self.num[i])
        return f"({type(self).__name__})(base = {self.base})({x})"
        
    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return self.numDigits
        
    def __getitem__(self, key):
        if key > self.numDigits:
            raise Exception("Overflow")
        return self.num[(MAX_SIZE - 1) - (len(self) - key)]

    def __add__(self, other):  
        Num.operateValidator(self,other)
        if self.base != other.base:
            raise Exception("Different Bases")
        else:
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
        Num.operateValidator(self,other)
        if self.base != other.base:
            raise Exception("Different Bases")
        else:
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
                        result.append(sum - (self.base * (sum//10)))
                        llevo = True
                        carry = sum // 10
                    else:
                        result.append(sum)
                        llevo = False
                c +=1
                result = result[::-1]
                total = total +  type(self)("".join(str(i) for i in result), self.base)
            return total

    def __floordiv__(self, other):
        Num.operateValidator(self,other)
        if self.base != other.base:
            raise Exception("Different Bases")
        else:
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
        Num.operateValidator(self,other)
        if self.base != other.base:
            raise Exception("Different Bases")
        else:
            result = self + ~other
            if self < other: result.is_complement = True
            return result

    def __invert__(self):   
        x = [ self.base - 1 - x for x in self.num ]
        result = type(self)("".join(str(i) for i in x), self.base) + type(self)(1, self.base)
        result.is_complement = True
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
        return self * type(self)(digits = 10**position, b =self.base)

    def __rshift__(self, position):
        return self // type(self)(digits = 10**position, b = self.base)

class Knum(Num):
    """
    def __mul__(self, other):
        # BASE CASE
        if len(self) <= 1 and len(other) <= 1:  
            return type(self)(digits = self[1]*other[1], b = self.base)
        else:
            # CALCULADING N/2 = NUMER OF DIGITS/2
            n = len(self) // 2 if len(self) >= len(other) else len(other) // 2
            #if n % 2 != 0 : n+=1
            # CALCULADING MIDDLE OF THE KNUMBER's
            mid_self = MAX_SIZE - len(self) // 2
            mid_other = MAX_SIZE - len(other) // 2
            # CREATING NEW KNUMBER's FROM THE PREVIOUS KNUMBER'S 
            a = type(self)("".join(str(i) for i in self.num[MAX_SIZE-len(self):mid_self]), self.base)
            b = type(self)("".join(str(i) for i in self.num[mid_self:]), self.base)
            c = type(other)("".join(str(i) for i in other.num[MAX_SIZE-len(other):mid_other]), other.base)
            d = type(other)("".join(str(i) for i in other.num[mid_other:]), other.base)
            # RECURSIVE CALL's (3 MULTIPLICATION's INSTEAD OF 4)
            ac = a*c
            bd = b*d
        return ac + bd
    """
if __name__=="__main__":
    
    print("-------- PRUEBAS INICIALES --------\n")
    print("\nSUMAS \n")
    
    x = 14
    y = "35"
    base3, base4, base7, base9, base10 = 3, 4, 7, 9, 10
    """ a = Num(x, base10)
    b = Num(y, base10)
    c = Num(x, base4)
    d = Num(y, base4)
    e = Knum(x, base7)
    f = Knum(y, base7)
    g = Knum(x, base9)
    h = Knum(y, base9)"""
    i = Num(x,4)
    j = Num(y,4)
    b = Num(123, base10)
    c = Num(123, base10)
    o = 12
    """  print(f"a = {a}")
    print(f"b = {b}")
    print(f"d = {d}")
    print(f"c = {c}")
    print(f"e = {e}")
    print(f"f = {f}")
    print(f"g = {g}")
    print(f"h = {h}")
    print(f"a+b = {a+b}")
    print(f"c+d = {a+b}")
    print(f"e+f = {a+b}")
    print(f"g+h = {a+b}")
    print(f"i+j = {i+j}")
    print(f"i+j = {i+j}")"""
    print(i+j)