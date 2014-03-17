

import argpext

def square(x):
    "Calculate the square of an argument"
    return x*x

class Square(argpext.Function):
    HOOK = square
    def populate(self,parser):
        parser.add_argument('x', default=0, type=float,
                            help='Specify the value of x.')


y = Square().digest(prog=None,args=['2'])
print( y )

y = Square()(x=2.0)
print( y )
