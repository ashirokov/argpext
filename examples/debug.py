#!/usr/bin/env python

import argpext

pri = argpext.DebugPrint()

def f():
    for i in range(100000):

        pri('here i=%d' % i,s=300,e=305,n=7)

        if argpext.debug.status(s=300,e=305,n=7)['live']:
            print( argpext.chainref() )


f()



