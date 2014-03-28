#!/usr/bin/env python

import sys
import ex


ex.Main1()(2)

ex.Main2()(3)

def fmt(value): return '[%s]' % value



print('--------------------')
for display in [False,True,{'stream': sys.stderr, 'str' : fmt  }]:
    print('display:',display)
    ex.Main1(display=display)(2)
    ex.Main2(display=display)(3)
    print()
