#!/usr/bin/env python

import argpext

class Dates(argpext.Function):
    "List dates in increasing order"

    @argpext.display
    def hook(self):
        for i in range(10000000000000):
            print('#',i)
            yield i

class Main(argpext.Node):
    SUBS = [('dates', Dates)]


if __name__ == '__main__':
    Main(True).digest()

