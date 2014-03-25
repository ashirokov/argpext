#!/usr/bin/env python

"""

Argpext: Hierarchical argument processing based on argparse.

Copyright (c) 2014 by Alexander V. Shirokov. This material
may be distributed only subject to the terms and conditions
set forth in the Open Publication License, v1.0 or later
(the latest version is presently available at
http://www.opencontent.org/openpub ).


"""

import sys
import time
import re
import os
import inspect
import argparse
import collections

VERSION = (2,0)

class Chdir(object):
    def __init__(self,path):
        self.initdir = os.getcwd()
        if not os.path.exists(path): os.makedirs(path)
        os.chdir(path)
    def __del__(self):
        os.chdir(self.initdir)



class KeyWords(object):
    "List of unique, ordered keywords"

    def __iadd__(self,keywords):
        for key in keywords:
            if not isinstance(key,str): raise TypeError()
            if key in self._dct: raise ValueError("repeating keyword: '%s'" % key)
            self._dct[key] = True # This value is always true

    def __init__(self,keywords=[]):
        self._dct = collections.OrderedDict()
        self += keywords

    def __len__(self):
        return len(self._dct)

    def __iter__(self):
        return reversed(list(self._dct.keys()))

    def __reversed__(self):
        return self._dct.keys().__reversed__()

    def __contains__(self,key):
        return self._dct.__contains__(key)

    def __call__(self,key):
        if key in self._dct: return key
        else: raise KeyError('invalid key: "%s"' % key)

    def __str__(self):
        q = list([ ("'%s'" % k) for k in self._dct.keys() ])
        q = '%s([%s])' % ( type(self).__name__, ','.join(q) )
        return q


E = KeyWords(['ARGPEXT_HISTORY'])


def frameref(fstr,up):
    "returns frame reference string"
    F = sys._getframe(1+up)
    path = F.f_code.co_filename
    basename = os.path.basename(path)
    lineno = F.f_lineno
    d = {
        'path' : path,
        'basename' : basename,
        'lineno' : lineno
    }
    return fstr % d


class Doc(object):
    def __init__(self,value):
        self.value = value
    def __call__(self,short=False,label=None):
        if self.value is None: return
        R = self.value
        if short is True:
            R = re.split('[\.;]',R)[0]

        debug = False
        if debug:
            R += '[%(position)s%(label)s]' % \
                 { 'position' : frameref('%(basename)s:%(lineno)s',up=1)
                   ,'label' : ('(%s)' % label  if label is not None else '') 
                 }

        return R



class BaseNode(object):

    def history_update(self,prog,args):
        "Update the history log file, if the latter is defined."
        filename = histfile()

        if not len(args): return

        if filename is not None:

            # Generate the logline
            timestr = time.strftime('%Y%m%d-%H:%M:%S', time.localtime())
            path = os.getcwd()
            cmd = ' '.join([prog]+args)


            logline = ','.join([ timestr, path, cmd ])+'\n'

            # Update the log file
            with open(filename,'a') as fho:
                fho.write( logline )

            # Truncate history file, if necesary
            size = os.stat(filename).st_size

            maxsize = 1024*1024
            if size > maxsize:

                cutsize = size-maxsize/2

                # Find: the remainder to be written to file
                remainder = ''
                with open(filename) as fhi:
                    cur = 0
                    while 1:
                        line = fhi.readline()
                        cur += len(line)
                        if cur >= cutsize: break
                    remainder = fhi.read()

                with open(filename,'w') as fhi:
                    fhi.write(remainder)


def get_func_defaults(func):
    "Populate D with the default values from the hook function"
    D = {}
    vs = func.__defaults__
    if vs is not None and len(vs):
        ns = func.__code__.co_varnames
        offset = len(ns)-len(vs)
        for i in range(offset,len(ns)):
            name = ns[i]
            value = vs[i-offset]
            D[name] = value
    return D

def get_parser_defaults( populate ):
    "Populate D with the default values from parser, except for those None."
    D = {}
    parser = argparse.ArgumentParser()

    populate( parser )

    # Populate the default values
    for k,v in parser._option_string_actions.items():
        if issubclass(type(v),argparse.Action):
            if isinstance(v,argparse._HelpAction): continue
            key = v.dest
            value = v.default
            D[key] = value

    return D



class Function(BaseNode):
    """Base class for command line interface to a Python function."""

    def __init__(self,bare=False):
        self.defaults = ['parser'] if not bare else []

    # Members to be overloaded by the user
    @staticmethod
    def hook():
        raise NotImplementedError()

    def populate(self,parser):
        """This method should be overloaded if hook takes
        positive number of arguments. The argument must be
        assumed to be of argparse.ArgumentParser type. For
        each argument, say 'x' of the hook method there must be a
        call (or its equivalent) to the parser.add_argument
        method with dest='x'."""
        pass


    # Other members
    def get_defaults(self,defaults):
        """Returns the dictionary of default function argument values."""
        DEFAULTS = KeyWords(['hook','parser'])

        D = {}
        for default in defaults:
            if default == DEFAULTS('hook'):
                D.update( get_func_defaults( self.get_function() ) )
            elif default == DEFAULTS('parser'):
                D.update( get_parser_defaults( self.populate ) )
            else:
                raise KeyError('invalid source: "%s"' % src)
        return D


    def get_function(self):
        "Return a callable instance defined by the reference function"
        q = type(self).hook
        if sys.version_info[0:2] <= (2, 7,): q = q.__func__
        return q

    def __call__(self,*args,**kwds):
        """Executes the reference function based on the default values and the
        arguments passed."""

        K = self.get_defaults(defaults=self.defaults)

        K.update( kwds )

        return self.get_function()(*args,**K)

    def digest(self,prog=None,args=None):
        """Execute the reference function based on command line arguments
        (automatically set to sys.argv[1:] by default). The return
        value equals the value returned by the reference function.
        """

        # Assign the default values of arguments.
        if prog is None: prog = os.path.basename( sys.argv[0] )
        if args is None: args = sys.argv[1:]

        # Update the history
        BaseNode.history_update(self,prog=prog,args=args)
        
        # Find: docstring
        q = self.__doc__
        if q is None: q = self.hook.__doc__
        docstr = Doc(q)

        # Find keyword args to pass to function, based on command line arguments, args.
        q = argparse.ArgumentParser(  description=docstr(label='description') )
        self.populate( q )
        q = vars(argparse.ArgumentParser.parse_args(q,args))

        # How are the default used?

        # Execute the reference function
        return self.get_function()( **q )



class Node(BaseNode):
    """Command line interface for a node."""

    # Members to be redefined by a user

    SUBS = []

    def populate(self,parser):
        """This may be overloaded to define global variables at hte frame
        where class is being defined."""
        pass

    # Other members

    def digest(self,prog=None,args=None):
        """Execute the node based on command line
        argument *args*, which must be 
        :py:class:`list`, :py:class:`tuple`, or *None* (in
        which case it is automatically assigned to
        `=sys.argv[1:]`). The return value is identical to
        the return value of the reference function.
        """

        class Binding(object):
            def __init__(self,node):
                self._node = node
            def __call__(self,namespace):
                if not isinstance(namespace,argparse.Namespace): raise TypeError
                q = vars( namespace )
                del q[ _EXTRA_KWD ]
                return self._node.hook( **q )


        def add_subtasks(parser):
            nodes = {}
            subparsers = None

            attributename = 'SUBS'
            subs = getattr(self,attributename)

            for name,node in subs:
                nodes[name] = node

                if subparsers is None: subparsers = parser.add_subparsers(help='Description')

                if inspect.isfunction(node):
                    #print( 'node', node )
                    #print( 'node', node.__name__ )
                    #print( 'node.__defaults__', node.__defaults__ )
                    #print( 'node.__globals__', str(node.__globals__)[:100] )
                    #print( 'varnames:', node.__code__.co_varnames )
                    #print( 'node', node.__name__.capitalize() )
                    node = type(node.__name__.capitalize(), 
                                (Function,) , 
                                {'hook' : staticmethod(node)
                                })


                if issubclass(node,Function):

                    q = getattr(node,'__doc__',None)
                    if q is None: q = node.hook.__doc__
                    docstr = Doc(q)
                    subparser = subparsers.add_parser(name,help=docstr(label='help',short=True),description=docstr(label='description') )
                    node().populate( subparser )
                    subparser.set_defaults( ** { _EXTRA_KWD : Binding(node) } )
                elif issubclass(node,Node):
                    N = node()
                    N._internal = True
                    docstr = Doc(getattr(node,'__doc__',None))
                    subparser = subparsers.add_parser(name,help=docstr(label='help',short=True),description=docstr(label='description') )
                    subparser.set_defaults( ** { _EXTRA_KWD : N } )
                else:
                    raise TypeError('invalid type (%s) for sub-command "%s" of %s' % ( node.__name__, name, type(self).__name__ ) )
            return nodes


        def delegation(args,parser,nodes):
            if len(args):
                word = args[0]
                node = nodes[word]

                if inspect.isfunction(node) or issubclass(node,Function):
                    q = argparse.ArgumentParser.parse_args( parser, args )
                    # Execute bound function.
                    return getattr(q,_EXTRA_KWD)( q )
                elif issubclass(node,Node):
                    q = argparse.ArgumentParser.parse_args( parser, [word] )
                    return getattr(q,_EXTRA_KWD).digest( prog='%s %s' % (prog,word) # chaining
                                                         , args=args[1:] )
                else:
                    raise TypeError



        if prog is None: prog = os.path.basename( sys.argv[0] )
        if args is None: args = sys.argv[1:]

        _EXTRA_KWD = '_ARGPEXT_EXTRA_KWD'


        # Write history file
        if not hasattr(self,'_internal'):
            BaseNode.history_update(self,prog=prog,args=args)


        # Find: rightparser, the parser for delegation tasks
        docstr = Doc(self.__doc__)

        rightparser = argparse.ArgumentParser( prog=prog, description=docstr(label='description')  )

        # Find: rightnodes, the lookup dict for delegation tasks
        rightnodes = add_subtasks(rightparser)

        # Find: leftargs,rightargs: argument splitting
        leftargs = []
        rightargs = []
        current = leftargs
        for i,arg in enumerate(args):
            if len(rightargs) or arg in rightnodes: current = rightargs
            current += [arg]

        # Find: leftparser, parser for flat level tasks: either before delegation or to print help.
        docstr = Doc(self.__doc__)

        leftparser = argparse.ArgumentParser( prog=prog, description=docstr(label='description')  )
        add_subtasks(leftparser)

        # Populate left parser with flat level tasks
        self.populate( leftparser )

        # Execute flat level tasks (setting the global variables)
        namespace = argparse.ArgumentParser.parse_args( leftparser, leftargs )
        for variable,value in vars(namespace).items():
            module = inspect.getmodule(self)
            setattr(module,variable,value)


        # Execute delegation level tasks.
        delegation(args=rightargs,parser=rightparser,nodes=rightnodes)


def histfile():
    "Returns file path of the hierarchical subcommand history file"
    varb = E('ARGPEXT_HISTORY')
    path = os.getenv(varb)
    return path



class History(Function):
    "Display command line history."

    @staticmethod
    def hook(unique):
        q = histfile()
        if not os.path.exists(q): 
            print('History file ("%s") not found' % q)
        else:
            lastcommand = None
            with open(q) as fhi:
                for line in fhi:
                    date,path,command = line.split(',',2)
                    if unique and lastcommand is not None and command == lastcommand: continue
                    print(line.rstrip())
                    lastcommand = command

    def populate(self,parser):
        parser.add_argument('-u',dest='unique',default=False,action='store_true',
                            help='Do not show repeating commands')



class Main(Node):
    "Hierarchical extension of argparse"
    SUBS = [('history', History)
            ]

if __name__ == '__main__':
    Main().digest()
