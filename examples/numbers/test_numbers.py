#!/usr/bin/env python

import argpext
from numbers import *

r1 = Numbers(display=True).digest(args=['-n', '5'])
r2 = Main(display=True).digest(args=['numbers', '-n','5'])
r3 = Numbers(display=True)(n=5)

for gn in [r1,r2,r3]:
    print('-'*90)
    for x in gn:
        print( 'x =', x )
