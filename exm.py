#!/usr/bin/env python

import ex


ex.Main1()(2)

ex.Main2()(3)

print('--------------------')
for display in [False,True]:
    print('display:',display)
    ex.Main1(display=display)(2)
    ex.Main2(display=display)(3)
    print()
