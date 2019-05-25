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

class AbstractNum:
    @abstractmethod
    def __add__() : pass
    
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
            
class Knum(Num):
    def __add__(self, other):
        return super().__add__(other)
   
if __name__=="__main__":
    
    print("-------- PRUEBAS INICIALES --------\n")
    print("\nSUMAS \n")
    
    x = 45
    y = "13"
    base3, base4, base7, base9, base10 = 3, 4, 7, 9,10
    a = Num(x, base10)
    b = Num(y, base10)
    c = Num(x, base4)
    d = Num(y, base4)
    e = Knum(x, base7)
    f = Knum(y, base7)
    g = Knum(x, base9)
    h = Knum(y, base9)
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
    print(f"i+j = {i+j}")"""
    print(f"i+j = {i+j}")
    print(f"i*j = {i*j}")