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
    print('Processing data...')

#class process(argpext.Task):
#    "Process data"
#    hook = argpext.hook(process)

class Main(argpext.Node):
    "Get the data and process."
    SUBS = [
        ('get-data', GetData),
        ('process-data', argpext.hook(process,display=True) )
        ]

if __name__ == '__main__':
    Main().digest()
