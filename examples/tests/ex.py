#!/usr/bin/env python

import argpext



class Fn(argpext.Function):
    "Task Main 1"

    @argpext.display
    def hook(self,contdate):
        print('A:', contdate)
        return contdate

    def populate(self,parser):
        parser.add_argument('contdate',type=int,help="Content date")

class Main(argpext.Node):
    "Get all"
    SUBS = [('m1', Fn)
            ]


if __name__ == '__main__':
    Main().digest()

