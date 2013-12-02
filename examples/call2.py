#!/usr/bin/env python

import argpext


class Task1(argpext.Task):
    "Task1 execution"
    def hook(self,a,b):
        print('Executing task1..')
        print('upper:',self.upper())
        print('a:',a)
        print('b:',b)

    def populate(self,parser):
        parser.add_argument('-a',help='Specify parameter a')
        parser.add_argument('-b',help='Specify parameter b')

class Task2(argpext.Task):
    "Task2 execution"
    def hook(self,x,y):
        print('Executing task2..')
        print('upper:', self.upper())
        print('x:',x)
        print('y:',y)

    def populate(self,parser):
        parser.add_argument('-x',help='Specify parameter x')
        parser.add_argument('-y',help='Specify parameter y')


def func():
    print('executing func..')
    return 3

#Task()(a=1,b=2,c="des")

class Main(argpext.Node):
    SUBS = [('task1', Task1),
            ('task2', Task2),
            ('task3', func) # Passing a simple function
            ]
    def populate(self,parser):
        parser.add_argument('-n',type=int,help='Specify n')
        parser.add_argument('--debug',action='store_true',help='Specify debug mode')
        
if 1:
    if __name__ == '__main__':
        Main().digest()
else:
    Main()('--debug','task1',n=5)(a=3)

