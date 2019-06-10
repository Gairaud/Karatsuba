import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append("NumTypes")
from NumTypes import Knum
from NumTypes import Num
from NumTypes import AbstractNum
from NumTypes import SSNum

if __name__=="__main__":
    
    
    a = Num(178, 10)
    b = Num(3433, 10)
    c = Knum(12222, 10)
    d = Knum(34565, 10)
    e = SSNum(1678, 10)
    f = SSNum(365, 10)
    print("----------TESTING SOME OPERATIONS WITH DIFFERENT NUMTYPES-----------")
    print(a+b)
    print(c*d)
    print(e-f)
  
    
