#!/usr/bin/env python3

import sys, os


ps1 = '>>>'
ps2 = '...'

def notraceback(q):
    L = []
    if len(q):
        q = q.splitlines()
        for q in q:
            if q.startswith('Traceback '): continue
            if q.startswith(' '): continue
            L += [q]
    q = os.linesep.join(L)
    if len(q): q += os.linesep
    return q

class SS:

    def __init__(self,label):
        self._string = ''
        self._label = label

    def flush(self):
        pass

    def write(self,str):
        self._string += str

    def __repr__(self):
        if self._label == 'stdout':
            return "<_io.TextIOWrapper name='<stdout>' mode='w' encoding='UTF-8'>"
        elif self._label == 'stderr':
            return "<_io.TextIOWrapper name='<stderr>' mode='w' encoding='UTF-8'>"

    def __str__(self):
        return self._string


import code

script = sys.argv[1]
cons = code.InteractiveConsole()

with open(script) as fh:

    start = [
        "__name__ = '__main__'"
        ,"import sys"
        ,"sys.argv = ['eggs.py']"
        ,'del sys'
        ]
    for q in start:
        cons.push(q)

    for line in fh:

        line = line.rstrip()


        stdout = SS('stdout')
        stderr = SS('stderr')

        sys.stdout = stdout
        sys.stderr = stderr

        status = cons.push(line)

        prompt = ps2 if status else ps1



        q = sys.__stdout__
        q.write('%s %s' % ( prompt, line )+os.linesep )
        q.write(str(sys.stdout))
        q.write(notraceback(str(sys.stderr)))




