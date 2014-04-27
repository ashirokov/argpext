#!/usr/bin/env python

import sys, traceback
import argpext

pre = argpext.DebugPrint()

class Task(argpext.Task):
    def hook(self,a,debug,b="hooks default for b",c="hooks default for c",dest="dest value"):
        print('Executing task 1..')
        print('a:',a)
        print('b:',b)
        print('c:',c)
        print('dest:',dest)
        print('debug:',debug)

    def populate(self,parser):
        parser.add_argument('a', help="Value of a")
        parser.add_argument('-b', help="Value of b")
        parser.add_argument('-c', default="parsers default for c", help="Value of c. The default is %(default)s.")
        parser.add_argument('--dest', help="Value of dest.")
        parser.add_argument('--debug',action='store_true', help="The debug mode.")


if 1:

    Task()('dest value','--debug',dest=2343)

else:

    try:
        Task().digest()
    except:
        a,b,c = sys.exc_info()
        traceback.print_tb( c )








