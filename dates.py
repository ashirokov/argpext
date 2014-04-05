#!/usr/bin/env python

import argpext

class Dates(argpext.Function):
    "List dates in increasing order"

    @argpext.display
    def hook(self):
        for i in range(1000000000):
            print('#',i)
            yield i



if __name__ == '__main__':
    Dates(True).digest()

