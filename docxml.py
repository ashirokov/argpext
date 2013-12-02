#!/usr/bin/env python

import argparse
import shutil
import os
import io
import sys
import subprocess
import code
import xml, xml.dom.minidom




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



def scriptrun(command,outputfile,interpreter_flags):


    def prn(line,file):
        file.write(line)
        file.write(os.linesep)

    interpreter = sys.executable

    cmd = [interpreter]+interpreter_flags+command.split()

    #print(cmd,file=sys.__stdout__)

    proc = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE )
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

    prefix = '' if not interpreter_flags else ' '.join([os.path.basename(interpreter)]+interpreter_flags)+' '

    prm = '$ '+prefix+command+os.linesep

    output = prm+so+se

    fho = open(outputfile,'w')

    #sys.stdout.write('Writing file: %s\n' % outputfile)
    #print( sys.path )

    fho.write( output )
    print( output )

    fho.close()




def interp(fhi,outputfile):

    def pnl(q):
        if len(q): q += os.linesep
        return q

    sys.__stdout__.write('Writing the file: %s\n' % outputfile)

    cons = code.InteractiveConsole()

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
        
        fho.write( output )
        sys.__stdout__.write( output )

    fho.close()



def xmlgen(filename):

    attr = (lambda *x: getattr(x[0].attributes.get(x[1]),'value',x[2]) )

    dom = xml.dom.minidom.parse( filename )
    dom = dom.childNodes[0]

    outputdir = attr(dom,'outputdir',os.getcwd())
    if not os.path.exists(outputdir): os.makedirs(outputdir)

    for cn in dom.childNodes:

        if isinstance(cn,xml.dom.minidom.Text) : continue

        def parse_interp(dom):
            q = attr(dom,'output',None)
            outputfile = os.path.join(outputdir,q)

            q = attr(dom,'source',None)
            if q is not None:
                q = open(q)
            else:
                q = dom.childNodes[0].data.strip()
                q = io.StringIO(q)
            interp(fhi=q,outputfile=outputfile)
            q.close()

        def parse_script(dom):
            q = attr(dom,'output',None)
            outputfile = os.path.join(outputdir,q)

            command = attr(dom,'command',None)
            q = attr(dom,'interpreter_flags',None)
            interpreter_flags = q.split() if q is not None else []

            scriptrun(command,outputfile,interpreter_flags)
            return outputfile

        def parse_copy(dom):
            path = attr(dom,'output',None)
            if os.path.samefile(os.getcwd(),path): return
            inputfile = path
            outputfile = os.path.join(outputdir,path)
            shutil.copy(src=inputfile,dst=outputfile)
            return outputfile

        def pad(ch,title):
            nleftpad = 5
            nmax = 70
            s = '%s %s ' % (ch*nleftpad, title )
            nrem = nmax-len(s)
            if nrem > 0:
                s += ch*nrem 
            return s

        print( pad('#', ("processing: %s" % cn.tagName) ) )

        outputfile = {'interp' : parse_interp, 
                      'script' : parse_script,
                      'copy' : parse_copy
                      }[ cn.tagName ](cn)

        print( pad(':', ('wrote: %s' % outputfile) ) )
        print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('xmlfile',help="xml file")
    a = parser.parse_args()
    xmlgen( a.xmlfile )

