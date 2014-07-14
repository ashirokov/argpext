from argpext import *

def f(m,n):
    "Return list of integers m to n"
    return list(range(m,1+n))

class F(Task):

    hook = customize(tostring=str)(s2m( f ))

    def populate(self,parser):
        parser.add_argument('m',type=int,help="Specify the value of M.")
        parser.add_argument('-n',type=int,default=3,
                            help="Specify the value of N; the default is %(default)s.")

if __name__ == '__main__':
    F().tdigest()
