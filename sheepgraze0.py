#!/usr/bin/env python3

import argparse

def sheep_graze(feed):
    print('Sheep grazes on %s' % feed)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Let sheep graze')
    parser.add_argument('-f', dest='feed', default='grass', 
                        help='Specify the feed. Default: %(default)s.')
    argv = parser.parse_args()

    sheep_graze(feed=argv.feed)
