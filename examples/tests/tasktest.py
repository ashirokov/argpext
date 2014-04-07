#!/usr/bin/env python

import itertools
import argpext

SEQUENCE = [1,2]

def gnr():
    for i in range(3):
        yield i

def func():
    return list([i for i in gnr()])


prn = argpext.DebugPrintOn('# %(pybasename)s %(lineno)s:')

def tasktest():
    for task,display,isstatic in itertools.product([gnr,func],[False,True],[False,True]):
        print('-'*120)
        print(task,display,isstatic)
        if isstatic:
            t = type('T',(argpext.Task,), {'HOOK' : task})(display=display)
        else:
            t = type('T',(argpext.Task,), {'hook' : argpext.hook(task,display=display)})(display=display)

        prn( t )

        for i in t():
            prn( i )


tasktest()


