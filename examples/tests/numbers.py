#!/usr/bin/env python

import argpext

SEQUENCE = [1,2]

class Gn(argpext.Function):
    "List numbers in increasing order"
    @argpext.display
    def hook(self):
        for i in SEQUENCE:
            yield i

class Fn(argpext.Function):
    "List numbers in increasing order"
    @argpext.display
    def hook(self):
        return SEQUENCE


class Main(argpext.Node):
    SUBS = [('gn', Gn),
            ('fn', Fn),
            ]


if __name__ == '__main__':
    Main().digest()

    
