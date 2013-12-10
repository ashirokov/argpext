#!/usr/bin/env python3

"""

Argpext: Hierarchical argument processing based on argparse.

Copyright (c) 2012 by Alexander V. Shirokov. This material
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


class Categorical(object):
    """Categorical variable type."""

    class Unit(object):
        "Value unit for Categorical variables."
        def __init__(self,value,help=None,callable=False):
            self._value = value
            assert(isinstance(help,(str,type(None),) ))
            self._help = help
            self._callable = callable
            assert(isinstance(callable,bool))
        def __call__(self):
            return self._value() if self._callable else self._value

        evaluate = __call__ # For backward compatibility with argpext-1.1 only


    def __init__(self,keys=()):
        L = []
        for q in keys:
            if not isinstance(q,str): raise TypeError()
            item = (q, Categorical.Unit(value=q))
            L += [ item ]

        self.__dict = collections.OrderedDict(L)

    def __str__(self):
        K = []
        for key,choice in self.__dict.items():
            K += [key]
        return '{%s}' % ( '|'.join(K) )

    def __call__(self,key):
        "Finds and returns value associated with the given key."
        if key in self.__dict:
            unit = self.__dict[key]
            return unit()
        else:
            raise KeyError('unmatched key: "%s".' % (key) )

    def items(self):
        return self.__dict.items()
    def __iter__(self):
        return self.__dict.__iter__()
    def keys(self):
        return self.__dict.keys()
    def values(self):
        return self.__dict.values()
    def __contains__(self,key):
        return self.__dict.__contains__(key)



class InitializationError(Exception): pass


E = Categorical(['ARGPEXT_HISTORY'])


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
        """Update the history file, if one if defined."""
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


class Function(BaseNode):
    """Base class for command line interface to a Python function."""

    # Members to be redefined by a user
    @staticmethod
    def HOOK():
        raise NotImplementedError()

    def populate(self,parser):
        """This method should be overloaded if HOOK takes
        positive number of arguments. The argument must be
        assumed to be of argparse.ArgumentParser type. For
        each argument X of the HOOK method there must be a
        call (or its equivalent) to the parser.add_argument
        method with dest='X'."""
        pass


    # Other members

    def defaults(self):
        """Returns the dictionary of command line default
        values of arguments."""

        # First, take the default values of function
        def update_func_defaults(D):
            "Populate D with the default values from HOOK function"
            q = self.HOOK
            vs = q.__defaults__
            if len(vs):
                ns = q.__code__.co_varnames
                offset = len(ns)-len(vs)
                for i in range(offset,len(ns)):
                    name = ns[i]
                    value = vs[i-offset]
                    D[name] = value

        def update_parser_defaults(D):
            "Populate D with the default values from parser, except for those None."
            parser = argparse.ArgumentParser()

            self.populate( parser )

            # Populate with default values
            for k,v in parser._option_string_actions.items():
                if issubclass(type(v),argparse.Action):
                    if isinstance(v,argparse._HelpAction): continue
                    key = v.dest
                    value = v.default
                    D[key] = value


        D = {}
        #update_func_defaults(D)
        update_parser_defaults(D)
        return D


    def __callable(self):
        q = type(self).HOOK
        return q.__func__ if sys.version_info[0:2] <= (2, 7,) else q

    def __call__(self,*args,**kwds):
        """Execute the reference function based on command line
        level default values of arguments and the values
        *args* and *kwds* given in the argument list. The
        return value is identical to the return value of the
        reference function."""
        kwds0 = self.defaults()
        for key,value in kwds.items():
            kwds0[key] = value
        return self.__callable()(*args,**kwds0)

    def digest(self,prog=None,args=None):
        """Execute the reference function based on command line
        argument *args*, which must be 
        :py:class:`list`, :py:class:`tuple`, or *None* (in
        which case it is automatically assigned to
        `=sys.argv[1:]`). The return value is identical to
        the return value of the reference function.
        """
        if prog is None: prog = os.path.basename( sys.argv[0] )
        if args is None: args = sys.argv[1:]
        BaseNode.history_update(self,prog=prog,args=args)

        q = self.__doc__
        if q is None: q = self.HOOK.__doc__
        docstr = Doc(q)

        q = argparse.ArgumentParser(  description=docstr(label='description') )
        self.populate( q )
        q = argparse.ArgumentParser.parse_args(q,args)
        q = vars(q)
        return self.__callable()( **q )



class Node(BaseNode):
    """Command line interface for a node."""

    # Members to be redefined by a user

    SUBS = []

    def populate(self,parser):
        """This may be overloaded """
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
                return self._node.HOOK( **q )


        def add_subtasks(parser):
            nodes = {}
            subparsers = None

            attributename = 'SUBS'
            subs = getattr(self,attributename,None)
            if subs is None:
                raise InitializationError('mandatory attribute %s is not defined for class %s' % (  attributename , type(self).__name__ ) )

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
                                {'HOOK' : staticmethod(node)
                                })


                if issubclass(node,Function):

                    q = getattr(node,'__doc__',None)
                    if q is None: q = node.HOOK.__doc__
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
                    raise InitializationError('invalid type (%s) for sub-command "%s" of %s' % ( node.__name__, name, type(self).__name__ ) )
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

        # Execute flat level tasks
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
    if path is None: raise KeyError('Variable %s is undefined' % varb)
    return path



class History(Function):
    "Display command line history."

    @staticmethod
    def HOOK(unique):
        q = histfile()
        if not os.path.exists(q): 
            print('history file is not found: %s' % q)
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
