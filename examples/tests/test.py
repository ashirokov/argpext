#!/usr/bin/env python

import sys
import argpext

prn = argpext.DebugPrintOn(prefix='| ')

def test_numbers():
    prn('#'*120)

    import numbers

    PAIRS = [(numbers.Gn, 'gn'),
             (numbers.Fn, 'fn')
             ]

    E = []
    for pair in PAIRS:
        C,word = pair
        E += [C(display=True).digest()]
        E += [C(display=True)()]
        E += [numbers.Main(display=True).digest(args=[word])]


    for L in E:
        prn('-'*90)
        prn('L:',L, type(L))
        for x in L:
            prn( 'x =', x )




def test_ex():
    prn('#'*120)

    import ex

    def fmt(value):
        return 'FMT%s' % value

    for display in [False,True,{'stream': sys.stderr, 'str' : fmt  }]:
        prn('display=%s' % display)
        for x in ex.Fn(display=display)():
            prn('x:',x)



test_numbers()

test_ex()









