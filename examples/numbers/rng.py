#!/usr/bin/env python

"Range test"

import copy
import argpext

SEQUENCE = [1,2,3]

def function():
    L = copy.copy(SEQUENCE)
    return L

def generator():
    for n in L:
        yield n


class Tester(argpext.Function):
    pass

