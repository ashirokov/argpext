#!/usr/bin/env python

import argpext

class Numbers(argpext.Function):
    "List numbers in increasing order"

    @argpext.display
    def hook(self):
        for i in range(5):
            print('#',i)
            yield i

class Root(argpext.Node):
    SUBS = [('numbers', Numbers)]


Numbers(display=True).digest(args=[])

Root(display=True).digest(args=['numbers'])

for i in Numbers()():
    print('i:',i)

