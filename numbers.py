#!/usr/bin/env python

import argpext

class Numbers(argpext.Function):
    "List numbers in increasing order"

    @argpext.display
    def hook(self,n):
        for i in range(n):
            yield i

    def populate(self,parser):
        parser.add_argument('-n',type=int, help="")


class Main(argpext.Node):
    SUBS = [('numbers', Numbers),
            ]

if __name__ == '__main__':
    Main().digest()

    
