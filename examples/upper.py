#!/usr/bin/env python

import argpext

class GetData(argpext.Task):
    "Get the data"

    def hook(self,name):
        print('Get %s data from database' % name)

    def populate(self,parser):
        parser.add_argument('-p', dest='name', default='sheep', 
                            type=argpext.KeyWords(['stock','bond']),
                            help='Data identifier. Choose from %(type)s. Default:"%(default)s".')

def process():
    print('Processing data ...' )
    return 1

class Process1(argpext.Task):
    "Process data"
    hook = argpext.make_hook(process,display=True)

class Process2(argpext.Task):
    "Process data"
    hook = process  # Illegal use



class Main(argpext.Node):
    "Get the data and process."
    SUBS = [
        ('get-data', GetData),
        ('process', process ),
        ('process1', Process1 ),
        ('process2', Process2 ),
        ]

if __name__ == '__main__':
    Main(verb=True).digest()

