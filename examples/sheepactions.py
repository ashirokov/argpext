#!/usr/bin/env python3

# File: sheepactions.py
import argpext

def sheep_graze(feed):
    print('Sheep grazes on %s' % feed)

class SheepGraze(argpext.Function):
    "Let sheep graze"
    HOOK = sheep_graze
    def populate(self,parser):
        parser.add_argument('-f', dest='feed', default='grass', 
                            help='Specify the feed. Default: %(default)s.')


def sheep_jump(n):
    print('Sheep jumps %d times' % n)

class SheepJump(argpext.Function):
    "Let sheep jump"
    HOOK = sheep_jump
    def populate(self,parser):
        parser.add_argument('-n', dest='n', default=2, type=int, 
                            help='Specify the number of jumps')


class Sheep(argpext.Node):
    "Sheep-related tasks"
    SUBS = [('graze', SheepGraze),  # Link subcommand 'graze' to class SheepGraze
            ('jump', SheepJump),    # Link subcommand 'jump'  to class SheepJump
            # Add more subcommands here
            ]


if __name__ == '__main__':
    Sheep().digest()

