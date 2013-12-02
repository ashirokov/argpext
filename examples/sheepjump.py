#!/usr/bin/env python3

import argpext

def sheep_jump(n):
    print('Sheep jumps %d times' % n)

class SheepJump(argpext.Function):
    "Make sheep jump"
    HOOK = sheep_jump
    def populate(self,parser):
        parser.add_argument('-j', dest='n', default=2, type=int, help='Specify the number of jumps')

if __name__ == '__main__':
    SheepJump().digest()
