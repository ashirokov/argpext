
import argpext

import os
import sys
import subprocess
import code



class Workdir(object):

    PATHS = ['PYTHONPATH','PATH']

    def __init__(self,dirname):
        self.dirname = dirname

    def __enter__(self):
        self.init_dir = os.path.abspath( os.getcwd() )
        self.target_dir = os.path.abspath( self.dirname )

        # Deal with sys.path
        self.path_init = sys.path
        self.path_mod = [self.target_dir]+[self.init_dir]+sys.path
        sys.path = self.path_mod

        # Deal with: PYTHONPATH
        self.epath = {}
        for k in self.PATHS:
            q = os.environ.get(k,None)
            self.epath[k] = q
            q = q.split(os.path.pathsep) if q is not None else []
            q = [self.init_dir]+q
            q = os.path.pathsep.join(q)
            os.environ[k] = q

        os.chdir( self.dirname )
        return self


    def __exit__(self, exc_type, exc_value, traceback):
        os.chdir( self.init_dir )

        for k in self.PATHS:
            q = self.epath.get(k)
            if q is None:
                del os.environ[k]
            else:
                os.environ[k] = q


        if sys.path != self.path_mod: raise ValueError('unexpected path')
        sys.path = self.path_init


        return False # Do not suppress exception



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


def filter_out_tr(q):
    "Filter out the traceback messages"
    L = []
    if len(q):
        q = q.splitlines()
        for q in q:
            if q.startswith('Traceback '): continue
            if q.startswith(' '): continue
            L += [q]
    q = os.linesep.join(L)
    return q



def scriptrun(interpreter,script,args,outputfile):


    def prn(line,file):
        file.write(line)
        file.write(os.linesep)


    prm = '$ '+' '.join( [script]+args )+os.linesep

    proc = subprocess.Popen( [interpreter]+[script]+args, stderr=subprocess.PIPE, stdout=subprocess.PIPE )

    proc.wait()

    L = []

    # Deal with stdout
    so = ''
    q = proc.stdout.read().decode()
    if len(q):
        q = q.splitlines()
        for q in q:
            q = q.replace('usage: ./','usage: ')
            so += (q+os.linesep)

    # Deal with stderr
    se = ''
    q = proc.stderr.read().decode()
    q = filter_out_tr(q)
    for line in q.splitlines():
        se += (line+os.linesep)

    output = prm+so+se

    fho = open(outputfile,'w')

    print('Writing file:', outputfile)
    #print( sys.path )

    fho.write( output )
    print( output )

    fho.close()




def interp(inputfile,outputfile):

    def pnl(q):
        if len(q): q += os.linesep
        return q

    print('Writing file:', outputfile,file=sys.__stdout__)

    cons = code.InteractiveConsole()

    fhi = open(inputfile)
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

        prompt = '... ' if status else '>>> '

        prm = '%s%s' % ( prompt, line )+os.linesep
        so = pnl(str(stdout))
        se = pnl(filter_out_tr(str(stderr)))
        output = prm+so+se

        fho.write( output )
        print( output, file=sys.__stdout__ , end='')

    fhi.close()
    fho.close()



