#!/usr/bin/env python

import argpext


class Main1(argpext.Function):
    "Task Main 1"

    @staticmethod
    def hook(contdate):
        print('A:', contdate)
        return contdate
    def populate(self,parser):
        parser.add_argument('contdate',type=int,help="Content date")


def func(contdate):
    print('A:', contdate)
    return contdate

class Main2(argpext.Function):
    "Task Main 2"
    hook = func
    def populate(self,parser):
        parser.add_argument('contdate',type=int,help="Content date")


class Main(argpext.Node):
    SUBS = [('m1', Main1),('m2', Main2)]

if __name__ == '__main__':
    Main().digest()

