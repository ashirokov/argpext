#!/usr/bin/env python

"""

Argpext: Hierarchical argument processing based on argparse.

Copyright (c) 2012,2014 by Alexander V. Shirokov. This material
may be distributed only subject to the terms and conditions
set forth in the Open Publication License, v1.0 or later
(the latest version is presently available at
http://www.opencontent.org/openpub ).


"""

import sys
import time
import re
import os
import warnings
import inspect
import argparse
import collections

VERSION = (1,2)

class ChDir(object):
    def __init__(self,path):
        self.initdir = os.getcwd()
        if not os.path.exists(path): os.makedirs(path)
        os.chdir(path)
    def __del__(self):
        try:
            os.chdir(self.initdir)
        except TypeError:
            pass
        except AttributeError:
            pass

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
        return self._dct.keys().__iter__()

    def __contains__(self,key):
        return self._dct.__contains__(key)

    def __call__(self,key):
        "Keyword lookup"
        if key in self._dct: return key
        else: raise KeyError('invalid key: "%s"' % key)

    def verify(self,keys):
        for key in keys:
            if key not in self: 
                raise KeyError("unrecognized key: '%s'" % key)


    def __str__(self):
        f = frameref(up=1)
        brief = (f['basename'] == 'argparse.py' and f['name'] == '_expand_help')
        if not brief:
            q = list([ ("'%s'" % k) for k in self._dct.keys() ])
            q = '%s([%s])' % ( type(self).__name__, ','.join(q) )
        else:
            q = list([ ("'%s'" % k) for k in self._dct.keys() ])
            if len(q) > 2:
                q[-1] = 'and '+q[-1]
            q = ', '.join(q)

        return q


ENVVARS = KeyWords(['ARGPEXT_HISTORY'])


def frameref(up=0):
    "returns frame reference string"
    frame = sys._getframe(1+up)
    code = frame.f_code
    lineno = frame.f_lineno
    path = code.co_filename
    name = code.co_name
    basename = os.path.basename(path)

    dirbasename = os.path.basename(os.path.abspath(os.path.dirname(path)))

    pybasename = os.path.join( * (([dirbasename] if basename.lower() == '__init__.py' else [])+[basename]) )

    return {
        'path' : path,
        'basename' : basename,
        'pybasename' : pybasename,
        'lineno' : lineno,
        'name' : name
    }


def chainref(fstr='%(name)s[%(pybasename)s:%(lineno)s]',sep=' < ',up=0,limit=None):
    "Return chain reference."
    i = 0
    L = []
    while 1:
        try:
            f = fstr % frameref(up=1+up+i)
        except ValueError:
            break
        L += [f]
        i += 1
        if limit is not None and i == limit: break
    return sep.join(L)

class DebugPrint(object):
    def __init__(self,prefix):
        self.prefix = prefix

class DebugPrintOff(DebugPrint):
    def __call__(self,*args,**kwds): pass

class DebugPrintOn(DebugPrint):
    def __call__(self,*args,**kwds): 
        frm = frameref(up=1)
        prefix = self.prefix % frm
        args = [ (str(a) % frm) for a in args ]
        args = [prefix]+args
        print(*args,**kwds)


pre = DebugPrintOff(prefix='EXECUTION: %(pybasename)s:%(lineno)s: ')
prt = DebugPrintOff(prefix='Task management: %(pybasename)s:%(lineno)s: ')
prd = DebugPrintOff(prefix='Debug: %(pybasename)s:%(lineno)s: ')

class Doc(object):
    def __init__(self,value):
        self.value = value
    def __call__(self,short=False,label=None):
        "Doc string presentation"
        if self.value is None: return
        R = self.value
        if short is True:
            R = re.split('[\.;]',R)[0]

        debug = False
        if debug:
            R += '[%(position)s%(label)s]' % \
                 { 'position' : '%(basename)s:%(lineno)s' % frameref(up=1)
                   ,'label' : ('(%s)' % label  if label is not None else '') 
                 }

        return R


VERB_KWDS = KeyWords(['stream','str'])

class BaseNode(object):

    def __init__(self,bare,verb,upper={}):
        self._bare = bare
        self._verb = verb
        self._upper = upper

    def upper(self):
        return self._upper

    def history_update(self,prog,args):
        "Update the history log file, if the latter is defined."
        filename = histfile()

        if not len(args): return

        if filename is not None:

            # Generate the logline
            def get_logline():
                timestr = time.strftime('%Y%m%d-%H:%M:%S', time.localtime())
                path = os.getcwd()
                cmd = ' '.join([prog]+args)
                logline = ','.join([ timestr, path, cmd ])+'\n'
                return logline

            def updatelog(filename,logline):
                MAX_LINESIZE = 1024
                MAX_FILESIZE = 1024*1024
                RETAIN_FILESIZE = MAX_FILESIZE/2

                def truncated_line(line,dots,size):
                    if len(line) > size:
                        dots = dots[0:size]
                        line = line[0:size]
                        line = line[0:(len(line)-len(dots))]+dots
                    return line

                def truncate_file(filename,max_filesize,retain_filesize):
                    if not ( 0 <= retain_filesize <= max_filesize ): raise ValueError()
                    initsize = os.stat(filename).st_size
                    cmlsize = 0
                    remove_trigger = ( initsize-max_filesize > 0)
                    retain_lines = []
                    if remove_trigger:
                        minimum_remove_size = initsize-retain_filesize
                        with open(filename) as fh:
                            for line in fh:
                                cmlsize += len(line)
                                if cmlsize >= minimum_remove_size:
                                    retain_lines += [line]
                            with open(filename,'w') as fh:
                                for line in retain_loines:
                                    fh.write( line )

            LINESEP = '\n'
            logline = get_logline()
            with open(filename,'a') as fh: fh.write( logline )
            updatelog(filename, logline)





def get_func_defaults(func):
    "Populate D with the default values from the function"
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


def verb_element(dspl,r,ignore_none):
    if dspl == False:
        return
    elif dspl == True:
        stream = sys.stdout
    elif isinstance(dspl,dict):
        try:
            for k in dspl: VERB_KWDS(k)
        except KeyError:
            raise KeyError('invalid key ("%s") in the the "dspl=" argument; allowed keys: %s' % (k, ",".join(['"%s"' % q for q in VERB_KWDS]) ))

        # Conditional convertion
        s = dspl.get('str',None)
        if s is not None: r = s( r )

        stream = dspl.get('stream',sys.stdout)
    else:
        raise TypeError('invalid type of display argument (neither bool not dict)')

    if r is None and ignore_none: pass
    else:
        stream.write( ('%s' % r)+'\n' )


def display(function):
    function._display = display
    return function


def make_hook(function,display=False):
    def wrapper(*args,**kwargs):
        self = args[0]
        args = args[1:]
        r = function(*args,**kwargs)
        return r
    if display: wrapper = globals()['display'](wrapper)

    # Propagate the doc
    q = getattr(function,'__doc__',None)
    if q is not None: wrapper.__doc__ = q

    return wrapper


def interwine(verb,r):
    if inspect.isgenerator(r):
        def wrapper():
            for rr in r:
                pre( chainref() )
                verb_element(verb, rr,ignore_none=False)
                yield rr
        return wrapper()
    else:
        verb_element(verb, r, ignore_none=True)
        return r


def execution(basenode,args,kwds):

    pre('%(name)s started')

    H,isstatic = basenode.get_hook()

    args = ((basenode,) if not isstatic else ())+args

    r = H(*args,**kwds)

    pre('hook returns:',r,type(r))
    pre( getattr(H,'_display',None) )

    if getattr(H,'_display',None) == display or isstatic:
        r = interwine(basenode._verb,r)
        pre('interwine returns:',r,type(r),chainref(limit=2))

    return r



_EXTRA_KWD = '_ARGPEXT_EXTRA_KWD'

class Binding(object):
    """Binding gets executed when functions variables are set by the
    parser, hence resulting in a namespace"""

    def __init__(self,funcobject):
        self._funcobject = funcobject

    def __call__(self,namespace):
        "Implicit execution, by parser."

        def get_kwds(namespace):
            if not isinstance(namespace,argparse.Namespace): raise TypeError
            q = vars( namespace )
            del q[ _EXTRA_KWD ]
            return q

        pre('execution: implicit via node')

        return execution( basenode=self._funcobject, args=(), kwds=get_kwds(namespace) )



class Task(BaseNode):
    """Base class for command line interface to a Python function."""

    def __init__(self,verb=True,bare=False,upper={}):
        BaseNode.__init__(self,verb=verb,bare=bare,upper=upper)

    # Members to be overloaded by the user
    def hook(self):
        raise NotImplementedError()

    def populate(self,parser):
        """This method should be overloaded if the function takes
        positive number of arguments. The argument must be assumed to
        be of argparse.ArgumentParser type. For each argument, say 'x'
        of the method there must be a call (or its equivalent) to the
        parser.add_argument method with dest='x'."""
        pass


    def get_hook(self):
        "Return a callable instance defined by the reference function"
        t = type(self)
        for attrname,isstatic in [('HOOK',True),
                                  ('hook',False)]:
            if hasattr(t,attrname):
                q = getattr(t,attrname)
                break
        if sys.version_info[0:2] <= (2, 7,): q = q.__func__
        return q,isstatic

    def __call__(self,*args,**kwds):
        """Direct execution, using Task class object"""
        #print('direct execution')

        def get_kwds(kwds):
            K = {}
            if not self._bare: K.update( get_parser_defaults( self.populate ) )
            # functions defaults will apply at this point
            K.update( kwds )
            return K

        # Explicit execution: invoked from a python script.
        pre('execution: explicit, in script')

        return execution( basenode=self, args=args, kwds=get_kwds(kwds) )


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
        if q is None: q = self.get_hook()[0].__doc__
        docstr = Doc(q)

        # Find keyword args to pass to function, based on command line arguments, args.
        def get_kwds(args):
            q = argparse.ArgumentParser(  description=docstr(label='description') )
            self.populate( q )
            K = vars(argparse.ArgumentParser.parse_args(q,args))
            return K

        # How are the default used?

        pre('execution: implicit, of Task, via digest')

        return execution( basenode=self, args=(), kwds=get_kwds(args) )



class Node(BaseNode):
    """Command line interface for a node."""

    def __init__(self,verb=True,bare=False,upper={}):
        BaseNode.__init__(self,verb=verb,bare=bare,upper=upper)

    # Members to be redefined by a user

    SUBS = []

    def populate(self,parser):
        """This may be overloaded to define global variables at the frame
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

        def add_subtasks(parser):
            subtasks = {}
            subparsers = None

            subs = getattr(self,'SUBS',[])

            for name,subtask in subs:
                subtasks[name] = subtask

                if subparsers is None: subparsers = parser.add_subparsers(help='Description')

                if inspect.isfunction(subtask):
                    prt("subtask is a function")
                    # Find: subtask, the class of the task.
                    subtask = type(subtask.__name__.capitalize(), 
                                (Task,) , 
                                {'hook' : make_hook(subtask,display=True)
                                })

                if issubclass(subtask,Task):

                    X = subtask(verb=self._verb,bare=self._bare,upper=self._upper)

                    q = getattr(subtask,'__doc__',None)
                    if q is None: q = X.get_hook()[0].__doc__
                    docstr = Doc(q)

                    subparser = subparsers.add_parser(name,help=docstr(label='help',short=True),description=docstr(label='description') )
                    X.populate( subparser )
                    subparser.set_defaults( ** { _EXTRA_KWD : Binding(funcobject=X) } )

                elif issubclass(subtask,Node):
                    X = subtask(verb=self._verb,bare=self._bare,upper=self._upper)
                    X._disable_history = True

                    docstr = Doc(getattr(subtask,'__doc__',None))

                    subparser = subparsers.add_parser(name,help=docstr(label='help',short=True),description=docstr(label='description') )
                    subparser.set_defaults( ** { _EXTRA_KWD : X } )
                else:
                    raise TypeError('invalid type (%s) for sub-command "%s" of %s' % ( subtask.__name__, name, type(self).__name__ ) )

            return subtasks


        def delegation(args,parser,nodes):
            if len(args):
                word = args[0]
                node = nodes[word]

                if inspect.isfunction(node) or issubclass(node,Task):
                    q = argparse.ArgumentParser.parse_args( parser, args )
                    # Execute bound function.
                    return getattr(q,_EXTRA_KWD)( q )
                elif issubclass(node,Node):
                    q = argparse.ArgumentParser.parse_args( parser, [word] )
                    # Chaining
                    return getattr(q,_EXTRA_KWD).digest( prog='%s %s' % (prog,word), args=args[1:] )
                else:
                    raise TypeError



        if prog is None: prog = os.path.basename( sys.argv[0] )
        if args is None: args = sys.argv[1:]


        # Write history file
        if not hasattr(self,'_disable_history'):
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

        # Find: upper, by executing flat level tasks
        namespace = argparse.ArgumentParser.parse_args( leftparser, leftargs )
        for variable,value in vars(namespace).items():
            self._upper[variable] = value

        # Execute delegation level tasks.
        return delegation(args=rightargs,parser=rightparser,nodes=rightnodes)


def histfile():
    "Returns file path of the hierarchical subcommand history file"
    varb = ENVVARS('ARGPEXT_HISTORY')
    path = os.getenv(varb)
    return path



class History(Task):
    "Display command line history."

    def hook(self,unique):
        q = histfile()
        if not os.path.exists(q): 
            sys.stderr.write(('History file ("%s") not found' % q)+os.linesep)
        else:
            lastcommand = None
            with open(q) as fhi:
                for line in fhi:
                    date,path,command = line.split(',',2)
                    if unique and lastcommand is not None and command == lastcommand: continue
                    sys.stdout.write(line.rstrip()+os.linesep)
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


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Backward compatibility with argpext version 1.1           !!
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

class Function(Task):
    def __init__(self,*args,**kwds):
        warnings.warn("Please rename all 'argpext.Function' into 'argpext.Task'. "\
                      "The support for argpext.Function may terminate starting from argpext Version 2.0"
                      , UserWarning)
        Task.__init__(self,*args,**kwds)

class Unit(object):
    "Value unit for Categorical variables."
    def __init__(self,value,help=None,callable=False):
        warnings.warn("Classes Categorical and Unit are now deprecated. "\
                          "Please use the new argpext.KeyWords class and standard pythons map to achieve the identical functionality."\
                          "The support for Unit may terminate starting from argpext Version 2.0"
                      , UserWarning)
        self._value = value
        assert(isinstance(help,(str,type(None),) ))
        self._help = help
        self._callable = callable
        assert(isinstance(callable,bool))
    def evaluate(self):
        return self._value() if self._callable else self._value


class Categorical(object):
    "Categorical variable type."""
    def __init__(self,mapping=(),typeothers=None):
        warnings.warn("Classes Categorical and Unit are now deprecated. "\
                          "Please use the new argpext.KeyWords class and standard pythons map to achieve identical effects."\
                          "The support for Unit may terminate starting from argpext Version 2.0"
                      , UserWarning)
        L = []
        count = 0
        for q in mapping:
            count += 1
            if isinstance(q,str): 
                item = (q, Unit(value=q))
            elif isinstance(q,(list,tuple)):

                if len(q) != 2: 
                    raise InitializationError('invalid size %d for %s item number %d' % ( len(q), type(q).__name__, count ) )

                if not isinstance(q[1],Unit):
                    q = [q[0],Unit(value=q[1])]
                item = q
            else:
                raise InitializationError('invalid type (%s) for mapping item number %d.' % ( type(q).__name__, count ) )
            L += [ item ]

        self.__dict = collections.OrderedDict(L)
        self.__typeothers = typeothers

    def __str__(self):
        K = []
        for key,choice in self.__dict.items():
            K += [key]

        q = self.__typeothers
        if q is not None:
            K += ['%s()' % q.__name__ ]

        return '{%s}' % ( '|'.join(K) )

    def __call__(self,key):
        "Finds and returns value associated with the given key."
        if key in self.__dict:
            return self.__dict[key].evaluate()
        else:
            if self.__typeothers is None:
                raise KeyEvaluationError('unmatched key: "%s".' % (key) )
            else:
                return self.__typeothers(key)

