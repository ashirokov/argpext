#!/usr/bin/env python

import argpext

SEQUENCE = [1,2]

class Fn(argpext.Function):
    "Task Main 1"

    @argpext.display
    def hook(self):
        return SEQUENCE

class Main(argpext.Node):
    "Get all"
    SUBS = [('m1', Fn)
            ]


if __name__ == '__main__':
    Main().digest()

