import os
import sys
import timeit

file_dir = os.path.dirname(__file__)
sys.path.append("NumTypes")
from NumTypes import Knum
from NumTypes import Num
from NumTypes import AbstractNum
from NumTypes import SSNum

def toComma(n):
    return str(n).replace(".",",") # str para convertir a string

def karatsuba(x,y):
	"""Function to multiply 2 numbers in a more efficient manner than the grade school algorithm"""
	if len(str(x)) == 1 or len(str(y)) == 1:
		return x*y
	else:
		n = max(len(str(x)),len(str(y)))
		nby2 = n / 2
		
		a = x / 10**(nby2)
		b = x % 10**(nby2)
		c = y / 10**(nby2)
		d = y % 10**(nby2)
		
		ac = karatsuba(a,c)
		bd = karatsuba(b,d)
		ad_plus_bc = karatsuba(a+b,c+d) - ac - bd
        
        	# this little trick, writing n as 2*nby2 takes care of both even and odd n
		prod = ac * 10**(2*nby2) + (ad_plus_bc * 10**nby2) + bd

		return prod
if __name__=="__main__":
    
    
    i = Num(710000000, 10)
    j = Num(3, 10)
    x = Knum(12345, 10)
    y = Knum(234, 10)
    o = SSNum(34663734534, 10)
    p = SSNum(34534, 10)
    print(i*j)
    print(x*y)
    print(o*p)
    timeN= timeit.timeit("x*y", globals=globals(), number=100)
    print (timeN)
    with open("Multiplication.csv", "w") as file: 
        file.write("n;Num;Knum;SSnum\n")
        for k in range(1,50,1):
            timeN= timeit.timeit("i*j", globals=globals(), number=100)
            timeK= timeit.timeit("x*y", globals=globals(), number=1)
            timeSS= timeit.timeit("o*p", globals=globals(), number=100)
            
            tSS = "{0:.5f}".format(timeSS)
            tk = "{0:.5f}".format(timeK)
            
            tN="{0:.5f}".format(timeN)
            file.write(f"{i};{tN};{tk};{tSS}\n") # la f es para no poner + para concatenar ileras 
    print("Listo!")
    
