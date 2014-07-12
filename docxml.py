#!/usr/bin/env python

import shlex
import stat
import shutil
import os
import io
import sys
import subprocess
import code
import xml, xml.dom.minidom

import argpext



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



def node_shell(node):
    command = node.childNodes[0].data.strip()


    def prn(line,file):
        file.write(line)
        file.write(os.linesep)

    cmd = shlex.split(command)

    proc = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True )
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


    prm = '$ '+command+os.linesep

    output = prm+so+se

    return output



def node_python(node):
    attr = (lambda *x: getattr(x[0].attributes.get(x[1]),'value',x[2]) )
    save_as = attr(node,'save_as',None)

    text = '#!/usr/bin/env python'+os.linesep+node.childNodes[0].data.strip()

    if save_as is not None:
        with open(save_as,'w') as fho:
            fho.write( text )
        os.chmod(save_as,stat.S_IXUSR|stat.S_IRUSR|stat.S_IWUSR)


    R = []
    def pnl(q):
        if len(q): q += os.linesep
        return q

    cons = code.InteractiveConsole()

    start = [
        "__name__ = '__main__'"
        ,"import sys"
        ,"sys.argv = ['excode.py']"
        ,'del sys'
        ]
    for q in start:
        cons.push(q)


    for line in text.splitlines():

        line = line.rstrip()

        stdout = io.StringIO()
        stderr = io.StringIO()

        with Reconnect(stdout=stdout,stderr=stderr):
            status = cons.push(line)
        stdout.seek(0)
        stderr.seek(0)


        prompt = '... ' if status else '>>> '

        prm = '%s%s' % ( prompt, line )+os.linesep
        so = pnl(str(stdout.read()))
        se = pnl(filter_out_tr(str(stderr.read())))
        output = prm+so+se
        #print('[%s]' % output)
        R += [output]

    return ''.join(R)



def xmlgen(inputfile,outputfile):

    input_file_text = open(inputfile).read()


    def process(text):
        try:
            dom = xml.dom.minidom.parseString(text)
        except:
            print( text, file=sys.stderr )
            raise ValueError('XML not well-formed, see above')
        q = dom
        node = q.childNodes[0]
        content = node.attributes.get('content').value
        text = {'shell' :  node_shell, 'python' : node_python }[content](node)
        return text



    def simple_parse():
        key = 'input'
        q = input_file_text
        C = q.split('</%s>' % key)
        N = len(C)
        T = []
        for i,c in enumerate(C):
            if i > 0 and i < N-1:
                left,right = c.split('<%s ' % key,1)
                T += [ left ]
                X = '<%s %s</%s>' % ( key, right, key )
                X = process(X)
                T += [X]
                print( X )
            else:
                T += [ c ]

    simple_parse()


class Main(argpext.Task):

    def hook(self,inputfile,outputfile):
        with argpext.ChDir('doc.tmp') as workdir:
            xmlgen( inputfile=os.path.join(workdir.initdir,inputfile), 
                    outputfile=os.path.join(workdir.initdir,outputfile) )

    def populate(self,parser):
        parser.add_argument('inputfile',help="Input rst file")
        parser.add_argument('outputfile',help="Output file")



if __name__ == '__main__':
    Main().digest()



