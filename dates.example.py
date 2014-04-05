#!/usr/bin/env python

import dates

import argpext

class Dates(argpext.Function):
    "List dates in increasing order"

    #@argpext.display
    def hook(self):
        for i in range(1000000000):
            print('#',i)
            yield i
            #pass



for i in Dates(display=True)():
    print('-=-',i)
    pass

