
import argpext

import os
import sys
import subprocess
import code

class StringStream(object):

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


PS1 = '>>>'
PS2 = '...'


def pnl(q):
    """For empty string return itself; for non-empty string return the
string finished by newline"""
    if len(q): q += os.linesep
    return q
    

def filter_out_tr(q):
    L = []
    if len(q):
        q = q.splitlines()
        for q in q:
            if q.startswith('Traceback '): continue
            if q.startswith(' '): continue
            L += [q]
    q = os.linesep.join(L)
    return q



def scriptrun(script,args,outputfile):

    print('writing exprog:', outputfile, file=sys.__stdout__)

    def prn(line,file):
        file.write(line)
        file.write(os.linesep)

    output = open(outputfile,'w')

    prn('$ '+' '.join( [script]+args ), file=output )

    proc = subprocess.Popen( [os.path.abspath(script)]+args, stderr=subprocess.PIPE, stdout=subprocess.PIPE )

    proc.wait()

    L = []

    # Deal with stdout
    q = proc.stdout.read().decode()

    if len(q): 
        q = q.splitlines()
        for q in q:
            q = q.replace('usage: ./','usage: ')
            prn(q, file=output)

    # Deal with stderr
    q = proc.stderr.read().decode()
    q = filter_out_tr(q)

    # display all
    for line in q.splitlines():
        prn( line, file=output )


    output.close()




class Reconnect(object):
    def __init__(self,stdout,stderr):
        self._so = sys.stdout
        self._se = sys.stderr
        sys.stdout = stdout
        sys.stderr = stderr

    def __enter__(self): pass

    def __exit__(self,exc_type, exc_value, traceback):
        sys.stdout = self._so
        sys.stderr = self._se
        return True # Suppresses the exception


def interp(input,outputfile):

    print('writing excode:', outputfile,file=sys.__stdout__)

    cons = code.InteractiveConsole()

    fhi = open(input)
    fho = open(outputfile,'w')

    start = [
        "__name__ = '__main__'"
        ,"import sys"
        ,"sys.argv = ['excode.py']"
        ,'del sys'
        ]
    for q in start:
        cons.push(q)

    for line in fhi:

        line = line.rstrip()

        stdout = StringStream('stdout')
        stderr = StringStream('stderr')

        with Reconnect(stdout=stdout,stderr=stderr):

            status = cons.push(line)

            prompt = PS2 if status else PS1

            fho.write('%s %s' % ( prompt, line )+os.linesep )
            fho.write( pnl(str(stdout)) )
            fho.write( pnl(filter_out_tr(str(stderr))) )

    fhi.close()
    fho.close()


