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

ACTIONS = argpext.KeyWords(['show','execute'])


class __NoDefault: pass

def get_nodeattr(node,key,default=__NoDefault()):
    if isinstance(default,__NoDefault):
        q = node.attributes.get(key)
        if q is None: raise ValueError('mandatory key value missing for %s' % key)
        return getattr(q,'value')
    else:
        return getattr(node.attributes.get(key),'value', default)


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



def process_shell(text):
    PATH_INI = os.getenv('PATH')
    os.environ['PATH'] = '%s%s%s' % (os.path.curdir,os.path.pathsep,PATH_INI)

    command = text

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

    os.environ['PATH'] = PATH_INI

    return output



def process_python(text):
    SYS_PATH_INI = sys.path
    sys.path = [os.path.curdir]+sys.path

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

    sys.path = SYS_PATH_INI

    return ''.join(R)


def parse_node(node):
    content = get_nodeattr(node,'content')
    action = ACTIONS(get_nodeattr(node,'action'))

    text = node.childNodes[0].data.strip()

    save_as = get_nodeattr(node,'save_as',None)
    if save_as is not None:
        with open(save_as,'w') as fho:
            fho.write( text )
        os.chmod(save_as,stat.S_IXUSR|stat.S_IRUSR|stat.S_IWUSR)


    if action == "show":
        pass
    elif action == "execute":
        text = {'shell' :  process_shell, 
                'python' : process_python,
                }[content](text)
    return text



def xmlgen(inputfile,outputfile,debug):


    def process(iline,text):
        print('processing....')
        try:
            dom = xml.dom.minidom.parseString(text)
        except:
            print( text, file=sys.stderr )
            raise ValueError('XML not well-formed, see above')

        node = dom.childNodes[0]

        text = parse_node(node)

        def f(text):
            T = []
            T = ['::']
            T += ['']
            for line in text.splitlines():
                T += ['    '+line]
            if debug:
                T += ['    ']
                T += ['    # File %s, line %d' % (os.path.basename(inputfile), iline)]
            T = '\n'.join(T)
            return T

        text = f(text)

        return text



    def simple_parse():
        chunk = []
        key = 'input'


        with open(outputfile,'w') as fho:

            write = (lambda x: print(x,file=fho))

            for iline,line in enumerate(open(inputfile),1):
                line = line.rstrip('\r\n')
                dump = None
                textline = None
                if len(chunk) == 0:
                    if line.startswith('<%s' % key):
                        chunk += [line]
                    else:
                        textline = line
                else:
                    chunk += [line]
                    if line.startswith('</%s>' % key):
                        dump = '\n'.join(chunk)
                        chunk = []


                print('[%d %s]' % ( iline, line) )

                if dump is not None:
                    q = process(iline,dump)
                    write( q )

                if textline is not None:
                    write(line)


    with argpext.ChDir('doc.tmp') as workdir:
        inputfile=os.path.join(workdir.initdir,inputfile)
        outputfile=os.path.join(workdir.initdir,outputfile)
        simple_parse()



class Main(argpext.Task):

    hook = argpext.make_hook(xmlgen)

    def populate(self,parser):
        parser.add_argument('-d',dest='debug',action='store_true',help="Debug mode")
        parser.add_argument('inputfile',help="Input rst file")
        parser.add_argument('outputfile',help="Output file")



if __name__ == '__main__':
    Main().digest()



