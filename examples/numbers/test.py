#!/usr/bin/env python

import sys
import argpext


def test_numbers():
    print('#'*120)

    import numbers

    PAIRS = [(numbers.Gn, 'gn'),
             (numbers.Fn, 'fn')
             ]

    L = []
    for pair in PAIRS:
        C,word = pair
        L += [C(display=True).digest()]
        L += [C(display=True)()]
        L += [numbers.Main(display=True).digest(args=[word])]


    for r in L:
        print('-'*90)
        print( 'r:',r )
        for x in r:
            print( 'x =', x )




def test_ex():
    print('#'*120)

    import ex

    print('--------------------')

    ex.Main().digest(['m1','2'])

    ex.Fn()(2)

    print('--------------------')

    def fmt(value):
        return '[%s]' % value

    for display in [False,True,{'stream': sys.stderr, 'str' : fmt  }]:
        print('display:',display)
        ex.Fn(display=display)(2)
        print()



test_numbers()
test_ex()









