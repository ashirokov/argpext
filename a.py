#!/usr/bin/env python

import inspect

def display(function):
    def wrapper(*args,**kwds):
        r = function(*args,**kwds)
        print('r:',r)
        if not inspect.isgenerator(r):
            print('|1|',r)
            return r
        else:
            for rr in r:
                print('|2|',rr)
                yield rr
    return wrapper


@display
def ls():
    R = [i for i in range(4)]
    return R

@display
def gn():
    for i in range(100000000):
        yield i


print('-'*100)

for i in ls():
    print('$', i )

print('-'*100)

for i in gn():
    print('$', i )

print('-'*100)
