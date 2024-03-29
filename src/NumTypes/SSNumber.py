"""
Authors:
1) Kevin Flores G             
2) Philippe Gairaud     

SSNum class
"""
from NaturalNumber import *

class SSNum(Num):
    def SimpleListSum(self,list1,list2):
        """
            Sum two list element per element

        """
        result = []
        SumCounter = len(list1)
        for x in range (SumCounter-1 ,-1, -1):
            sum = list1[x]+list2[x]
            result.append(sum)
        result = result[::-1]
        return result
    def __mul__(self,other):
        """
            Demo implementation of Schönhage–Strassen algorithm
            ***IMPLEMENTATION CAN BE IMPROVED***
        """
        if self.base != 10:
            raise Exception("SS is only defined for base 10")
        result = [0]
        zeros = [0]
        total = [0]*MAX_SIZE
        c = 0
        for x in range(MAX_SIZE-1, -1+c, -1):
            result = []
            result.extend(zeros*c)
            for y in range(MAX_SIZE-1, -1+c, -1):
                sum = self.num[y] * other.num[x]
                result.append(sum)
            total = self.SimpleListSum(result[::-1],total)
            c+=1
        def Recombination(self, result):
            """
                Products recombination
            """
            c = 1
            total = type(self)(0,self.base)
            for x in range (MAX_SIZE-1,-1,-1):
                total = type(self)(result[x]*c,self.base)+total
                c *= 10
            return total
        return Recombination(self,total)  