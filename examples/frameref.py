#!/usr/bin/env python

import argpext

def f():
    pre('F')


pre = argpext.DebugPrint()
pre('here: start')
f()
pre('here: done')



