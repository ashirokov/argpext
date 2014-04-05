#!/usr/bin/env python

import argpext
from numbers import *

Numbers(display=True).digest(args=['-n', '5'])
Main(display=True).digest(args=['numbers', '-n','5'])
for i in Numbers()(n=5):
    print('i:',i)

