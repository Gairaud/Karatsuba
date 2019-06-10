<<<<<<< HEAD
"""
Authors:
1) Kevin Flores G             
2) Philippe Gairaud     

Abstract class of Num
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
        others data types

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
=======
"""
Authors:
1) Kevin Flores G             
2) Philippe Gairaud     

Abstract class of Num
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
        others data types

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
>>>>>>> 23b713c724d376e691197d5e25e585da5f3de198
