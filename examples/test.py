#!/usr/bin/env python

import itertools
import argpext

def gnr():
    for i in range(2):
        yield i

def func():
    return list([i for i in gnr()])


prn = argpext.DebugPrint()

def tasktest():

    options = {
        'task' : [gnr,func],
        'verb' : [False,True],
        'isstatic' : [False,True],
        }

    keys = [
        'isstatic',
        'verb',
        'task',
        ]

    print('Test order: ', ', '.join(keys) )

    for itest,item in enumerate(itertools.product(*[options[k] for k in keys])):
        #if (itest != 2): continue
        print('-'*120)
        print('itest:',itest)
        x = [(key, item[i]) for i,key in enumerate(keys)]
        print('Parameters:', ', '.join(['%s:%s' % (a,b)  for a,b in x]) )
        x = dict(x)

        if x['isstatic']:
            T = type('Type0',(argpext.Task,), {'HOOK' : x['task']})
        else:
            T = type('Type1',(argpext.Task,), {'hook' : argpext.make_hook(x['task'],display=True) })

        t = T(verb=x['verb'])


        for i in t():
            prn( i )


tasktest()


