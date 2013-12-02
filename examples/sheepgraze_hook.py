#!/usr/bin/env python3

import argpext

class SheepGraze(argpext.Function):
    "Let sheep graze"

    @staticmethod
    def HOOK(feed):
        print('Sheep grazes on %s' % feed)

    def populate(self,parser):
        parser.add_argument('-f', dest='feed', default='grass', 
                            help='Specify the feed. Default: %(default)s.')

if __name__ == '__main__':
    SheepGraze().digest()

