#!/usr/bin/env python

# File: sheepgraze2.py
import argpext

def sheep_graze(quantity,feed,hours):
    print( ('%s of sheep grazes on %s for %.1f hours.' \
              % (quantity, feed, hours) ).capitalize() )

class SheepGraze(argpext.Function):
    "Let sheep graze"
    hook = argpext.hook(sheep_graze)
    def populate(self,parser):
        parser.add_argument(dest='quantity', help='Quantity of sheep.')
        parser.add_argument('-f', dest='feed', default='grass', 
                            help='Specify the feed. Default: %(default)s.')
        parser.add_argument('-t', dest='hours', default=2.5, type=float,
                            help='Specify number of hours. Default: %(default)s.')

if __name__ == '__main__':
    SheepGraze().digest()
