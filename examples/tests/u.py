#!/usr/bin/env python

import itertools
import argpext

SEQUENCE = [1,2]

def gnr():
    for i in range(3):
        yield i

def func():
    return list([i for i in gnr()])


prn = argpext.DebugPrintOn('# ')

def tasktest():
    for F,D in itertools.product([gnr,func],[False,True]):
        t = type('T',(argpext.Function,), {'hook' : argpext.hook(F,display=D)})(display=D)
        prn( t )
        for i in t():
            prn( i )


tasktest()


