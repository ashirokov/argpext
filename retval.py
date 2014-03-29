

import argpext

def square(x=1):
    "Calculate the square of an argument"
    return x*x

class Square(argpext.Function):
    hook = argpext.hook(square)
    def populate(self,parser):
        parser.add_argument('-x', default=2, type=float,
                            help='Specify the value of x.')

y = Square().digest(prog=None,args=['-x','2'])
print( y )

y = Square()(x=4)
print( y )

y = Square()()
print( y )

y = Square(bare=True)()
print( y )

