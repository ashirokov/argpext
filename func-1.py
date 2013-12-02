
from argpext import *

class F(Function):

    @staticmethod
    def HOOK(x,y,z):
        print('x,y,z:',x,y,z)
        return 0

    def populate(self,parser):
        parser.add_argument('-x',help='Value of x')
        parser.add_argument('-y',help='Value of y')
        parser.add_argument('-z',default=3,help='Value of z')



f = F()(x=1,y=2)
print(f )
