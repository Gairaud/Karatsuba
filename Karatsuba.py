"""
AUTORES:
1) Kevin Flores G             
2) Philippe Gairaud           
3) Oscar Ruiz V             
4) Kevin Delgado  
           
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
    def __div__(self, other) : pass
    @abstractmethod
    def __sub__(self, other) : pass
    @abstractmethod
    def __eq__(self,other) : pass
    @abstractmethod
    def __lt__(self, other) : pass
    @abstractmethod
    def __invert__(self) : pass 
    
class Num(AbstractNum):
    def __init__(self, digits = 0, b = Default_base):
        self.base = b
        numberList = [int(x) for x in str(digits)]
        self.numDigits = len(numberList)
        if self.numDigits > MAX_SIZE:
            raise Exception("Overflow")
        else: 
            self.num = [0] * MAX_SIZE
        for y in range(MAX_SIZE - self.numDigits, MAX_SIZE):
            self.num[y] = numberList.pop(0)
    
    def __str__(self):
        x = ""
        for i in range(MAX_SIZE-self.numDigits, MAX_SIZE):
            x += str(self.num[i])
        return f"({type(self).__name__})(base = {self.base})({x})"
        
    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return self.numDigits
        
    def __getitem__(self, key):
        if key > self.numDigits:
            raise Exception("Overflow")
        return self.num[(MAX_SIZE - 1) - (self.numDigits - key)]

    def __add__(self, other):  
        if self.base != other.base:
            raise Exception("Different Bases")
        else:
            result = []
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
            result = result[::-1]
            return type(self)("".join(str(i) for i in result), self.base)

    def __mul__(self, other):
        if self.base != other.base:
            raise Exception("Different Bases")
        else:
            result = []
            llevo = False
            total = Num(0,self.base)
            zeros = [0]
            c = 0
            for x in range(MAX_SIZE-1, -1+c, -1):
                result = []
                result.extend(zeros*c)
                for y in range (MAX_SIZE-1, -1+c, -1):
                    sum = self.num[y] * other.num[x]
                    if llevo: sum += 1
                    if sum >= self.base:
                        result.append(sum - self.base)
                        llevo = True
                    else:
                        result.append(sum)
                        llevo = False
                c +=1
                result = result[::-1]
                total = total +  type(self)("".join(str(i) for i in result), self.base)
            return total

    def __div__(self, other):
        if self.base != other.base:
            raise Exception("Different Bases")
        """
        else:
            result = []
            num = 0
            for x in range(MAX_SIZE - self.numDigits, MAX_SIZE):
                num += self.num[x]
                aux_1 = type(self)(digits = num, b = self.base)
                if  aux_1 >= other:
                    y = x
                    while y < MAX_SIZE:
                        multiply = 1
                        aux_2 = (type(self)(digits = multiply, b = self.base) * other                      
                        while aux_2 <= aux_1: 
                            multiply += 1
                            aux_2 = (type(self)(digits = multiply, b = self.base) * other
                        if aux_1 == aux_2 : result.append(multiply)
                        else: 
                            result.append(multiply-1)
                            aux_2 = (type(self)(digits = multiply - 1, b = self.base) * other
                        y += 1
                        if y < MAX_SIZE : 
                            aux_1 = (aux_1 - aux_2) 
                            aux_1 << 1
                            aux_1 = aux_1 + type(self)(digits=self.num[y], b = self.base)
                    break
            return type(self)("".join(str(i) for i in result), self.base)
        """

    def __sub__(self, other):
        
        if self.base != other.base:
            raise Exception("Different Bases")
        """
        else:
            if self.numDigits < other.numDigits : 
                bigger = other.num
                smaller = self.num
                negative = True
            else:
                bigger = self.num
                smaller = other.num
                negative = False
            result = []
            prestado = False
            for x in range(MAX_SIZE-1, -1, -1):
                resta = bigger[x] - smaller[x]
                if resta < 0 : prestado = True
                if prestado:
                    result.append(resta + self.base)
                    bigger[x - 1] -= 1
                else:
                    result.append(resta)
            result = result[::-1]
            total = type(self)("".join(str(i) for i in result), self.base)
            return ~total if negative else total
        """
        return self + ~other

    def __invert__(self):
        """
        x = [ self.base - 1 - x for x in self.num ]
        return type(self)("".join(str(i) for i in x), self.base) + type(self)(1, self.base)
        """
        result = type(self)(b = self.base)
        result.num = [ self.base - 1 - x for x in self.num ]
        aux = type(self)(1, self.base)
        result = result + aux
        return result

    def __eq__(self, other):
        if self.base != other.base:
            raise Exception("Different Bases")
        for x in range(MAX_SIZE-1,-1,-1):
            if self.num[x] != other.num[x] : return False
        return True

    def __lt__(self, other):
        if self.base != other.base:
            raise Exception("Different Bases")
        if self.numDigits > other.numDigits or self == other: return False
        elif self.numDigits == other.numDigits:
            for x in range(self.numDigits -1, -1, -1):
                k = self.num[MAX_SIZE - x - 1]*10**x
                y = other.num[MAX_SIZE - x - 1]*10**x
                if k > y: return False
        return True
    
    def __lshift__(self, position):
        return self * type(self)(10**position, self.base)

class Knum(Num):
    def __add__(self, other):
        return super().__add__(other)
   
if __name__=="__main__":
    
    print("-------- PRUEBAS INICIALES --------\n")
    print("\nSUMAS \n")
    
    x = 362
    y = "26"
    base3, base4, base7, base9, base10 = 3, 4, 7, 9, 10
    """ a = Num(x, base10)
    b = Num(y, base10)
    c = Num(x, base4)
    d = Num(y, base4)
    e = Knum(x, base7)
    f = Knum(y, base7)
    g = Knum(x, base9)
    h = Knum(y, base9)"""
    i = Num(x,base10)
    j = Num(y,base10)
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
    print(i/j)