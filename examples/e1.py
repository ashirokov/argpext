from argpext import *

# This is a standalone generator
def g(m,n):
    "Iterate over integers m to n"
    for i in range(m,1+n):
        yield i

class G(Task):

    hook = customize(tostring=str)(s2m( g ))

    def populate(self,parser):
        parser.add_argument('m',type=int,help="Specify the value of M.")
        parser.add_argument('-n',type=int,default=3,
                            help="Specify the value of N; the default is %(default)s.")


if __name__ == '__main__':
    G().tdigest()
