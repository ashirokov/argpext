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

    for itest,item in enumerate(itertools.product(*[options[k] for k in keys])):

        print('-'*120)
        print('itest:',itest)
        x = [(key, item[i]) for i,key in enumerate(keys)]
        print('Parameters:', ', '.join(['%s:%s' % (a,b)  for a,b in x]) )
        x = dict(x)

        if x['isstatic']:
            T = type('Type0',(argpext.Task,), {'HOOK' : x['task']})
        else:
            T = type('Type1',(argpext.Task,), {'hook' : argpext.hook(x['task'],display=x['display'])})

        t = T(display=x['display'])


        for i in t():
            prn( i )


tasktest()


