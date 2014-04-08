#!/usr/bin/env python

import itertools
import argpext

def gnr():
    for i in range(2):
        yield i

def func():
    return list([i for i in gnr()])


prn = argpext.DebugPrintOn('# %(pybasename)s %(lineno)s:')

def tasktest():

    options = {
        'task' : [gnr,func],
        'display' : [False,True],
        'isstatic' : [False,True],
        }

    keys = [
        'isstatic',
        'display',
        'task',
        ]

    print('Test order: ', ', '.join(keys) )

    for item in itertools.product(*[options[k] for k in keys]):

        print('-'*120)
        x = [(key, item[i]) for i,key in enumerate(keys)]
        print( x )
        x = dict(x)

        if x['isstatic']:
            t = type('T',(argpext.Task,), {'HOOK' : x['task']})(display=x['display'])
        else:
            t = type('T',(argpext.Task,), {'hook' : argpext.hook(x['task'],display=x['display'])})(display=x['display'])

        for i in t():
            prn( i )


tasktest()


