#!/usr/bin/env python

import argpext

import sheepactions # Module sheepactions is provided by previous example.



class FeedWolf(argpext.Task):
    "Feed the wolf"

    def hook(self,prey):
        print('Wolf eats %s' % prey)

    def populate(self,parser):
        parser.add_argument('-p', dest='prey', default='sheep', 
                            help='Specify the food. Default:"%(default)s".')

class Main(argpext.Node):
    "Top level sheepgame options"
    SUBS = [
        ('sheep', sheepactions.Sheep), # Attaching another Node
        ('feed-wolf', FeedWolf), # Attaching a Task
        # Add more subcommands here
        ]

if __name__ == '__main__':
    Main().digest()

