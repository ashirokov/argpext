#!/usr/bin/env python


import argpext

class A(argpext.Task):
    def hook(self,x,y):
        return (x,y)

print( A()(1,y=3) )
