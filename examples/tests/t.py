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


prn = argpext.DebugPrintOn('| ')

for i in Gn(display=True)():
    prn( i )

for i in Fn(display=True)():
    prn( i )
