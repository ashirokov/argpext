#!/usr/bin/env python3

import argpext

import sheepactions # Module sheepactions is provided by previous example.

def feed_wolf(prey):
    print('Wolf eats %s' % prey)

class FeedWolf(argpext.Function):
    "Feed the wolf"
    HOOK = feed_wolf
    def populate(self,parser):
        parser.add_argument('-p', dest='prey', default='sheep', 
                            help='Specify the food. Default:"%(default)s".')

class Main(argpext.Node):
    "Top level sheepgame options"
    SUBS = [
        ('feed-wolf', FeedWolf),      # Attaching a Function
        ('sheep', sheepactions.Sheep), # Attaching another Node
        # Add more subcommands here
        ]

if __name__ == '__main__':
    Main().digest()

