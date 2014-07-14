#!/usr/bin/env python

from argpext import *

def g(n):
    for i in range(n):
        yield i

class G(Task):
    hook = make_hook(g,display=1)
    def populate(self,parser):
        parser.add_argument('n',type=int,help='Set the number of iterations')



if __name__ == '__main__':
    for q in G().digest(transverse=False):
        pass
