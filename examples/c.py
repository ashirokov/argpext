from argpext import *

class T(Task):

    @customize(tostring=str)
    def hook(self,m,n):
        "Return list of integers m to n"
        return list(range(m,1+n))

    def populate(self,parser):
        parser.add_argument('m',type=int,help="Specify the value of M.")
        parser.add_argument('-n',type=int,default=3,
                            help="Specify the value of N; the default is %(default)s.")

if __name__ == '__main__':
    T().tdigest()

