#!/usr/bin/env python

import argpext

class Dates(argpext.Function):
    "List dates in increasing order"

    def hook(self,start):
        for i in range(1000000000):
            print(i)
            yield i



    def populate(self,parser):
        parser.add_argument('start',type=int,help="Starting number")


if __name__ == '__main__':
    Dates(True).digest()

