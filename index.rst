.. argpext documentation master file, created by
   sphinx-quick-start on Sun Sep 30 21:12:52 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Argpext |release| --- Documentation
===============================================================

.. module:: argpext

Argpext is a module dedicated to improving the command line
interface with Python module internals.  It allows one to
quickly expose any selected Python functions to the command
line within DOS or Linux-like shells. Help messages are
automatically produced.

Argpext provides hierarchical extension to the
"Sub-commands" utility of the standard :py:mod:`argparse`
module. It allows one to group any Python functions into a
hierarchical tree-like structure, e.g.  according to their
logic. Every such function then corresponds to a certain
sequence of sub-commands, and can be executed directly from
the command line by simply passing the sequence as command
line arguments to the top level script. The rest of the
command line arguments to the script are used to set up the
values of function arguments, at which level the standard
:py:mod:`argparse` interface applies.

Argpext provides a special variable type to support command
line arguments that take predetermined set of
values. Information about available choices is automatically
propagated into the usage help message.

The best way to learn Argpext is through an example. We
introduce Argpext through a series of illustrative examples
of tested programs. The formal :ref:`reference<reference>`
is at the bottom.

Argpext is an extension of :py:mod:`argparse`; its knowledge
is assumed in our document. 

.. _hierarchy_build:

Building the command line hierarchy
------------------------------------

In this section we build the sub-command hierarchy for an
application in order to establish the efficient connection
between the command line arguments and corresponding Python
functions. 

Bare bones example
^^^^^^^^^^^^^^^^^^

Consider a toy model of a sheep. 

As the bare bones example, suppose there is a function
called :func:`sheep_graze` that lets the sheep graze.  Here
is how we can use the standard :mod:`argparse` module in
order to connect this function to the command line:

<input content="python">
import argparse

def sheep_graze(feed):
    print('Sheep grazes on %s' % feed)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Let sheep graze')
    parser.add_argument('-f', dest='feed', default='grass', 
                        help='Specify the feed. Default: %(default)s.')
    argv = parser.parse_args()

    sheep_graze(feed=argv.feed)
</input>



The identical functionality is now achieved with our Argpext as follows:

.. _sheepgraze:

<input content="python" save_as="sheepgraze.py">
import argpext

def sheep_graze(feed):
    print('Sheep grazes on %s' % feed)

class SheepGraze(argpext.Task):
    "Let sheep graze"
    hook = argpext.make_hook(sheep_graze)
    def populate(self,parser):
        parser.add_argument('-f', dest='feed', default='grass', 
                            help='Specify the feed. Default: %(default)s.')

if __name__ == '__main__':
    SheepGraze().digest()
</input>


Class :class:`SheepGraze`, constructed by inheritance from
:class:`argpext.Task`, establishes the interface between
command line and function :func:`sheep_graze`.

Command line is processed during the call to the
:meth:`SheepGraze.digest` function.

The docstring ``"Let sheep graze"`` shows up inside the
usage. Indeed, when the above program is saved as file
``sheepgraze.py`` and executed with the ``--help`` or ``-h``
switches, we have:

.. _sheepgraze_usage:

<input content="shell">
sheepgraze.py -h
</input>


..
  
  Examples of execution

  Task :func:`sheep_graze` can be executed from the
  command line as follows:
  
<input content="shell">
sheepgraze.py
sheepgraze.py -f daisies
</input>

  Equivalently, in Python interpreter:

<input content="python">
import sheepgraze
sheepgraze.SheepGraze()()
sheepgraze.SheepGraze()(feed='daisies')
</input>



Adding a new sub-command
^^^^^^^^^^^^^^^^^^^^^^^^

Suppose we now wish to add another function
:func:`sheep_jump` to the :ref:`example<sheepgraze>` above.

First we should add a new class :class:`SheepJump` which is
completely analogous to the previously described
:class:`SheepGraze`.

Let us then introduce sub-commands ``graze`` and ``jump``. In
order to differentiate between the two different tasks on
the level of command line.

To provide the mapping between sub-commands ``graze`` and
``jump`` and their respective implementations
:func:`SheepGraze` and :func:`SheepJump` we declare class
:class:`Sheep` (subclass of :class:`argpext.Node`) and
assign the mapping to its :attr:`SUBS` attribute, as shown
in the example below. Tasks :func:`SheepGraze` and
:func:`SheepJump` are now attached to node :class:`Sheep`.

The next key thing is to include :meth:`Sheep.digest()` at
the bottom in order to execute command line on our new
interface.


.. _sheepactions:
<input content="python" save_as="sheepactions.py">
import argpext

def sheep_graze(feed):
    print('Sheep grazes on %s' % feed)

class SheepGraze(argpext.Task):
    "Let sheep graze"
    hook = argpext.make_hook(sheep_graze)
    def populate(self,parser):
        parser.add_argument('-f', dest='feed', default='grass', 
                            help='Specify the feed. Default: %(default)s.')


def sheep_jump(n):
    print('Sheep jumps %d times' % n)

class SheepJump(argpext.Task):
    "Let sheep jump"
    hook = argpext.make_hook(sheep_jump)
    def populate(self,parser):
        parser.add_argument('-n', dest='n', default=2, type=int, 
                            help='Specify the number of jumps')


class Sheep(argpext.Node):
    "Sheep-related tasks"
    SUBS = [('graze', SheepGraze),  # Link subcommand 'graze' to class SheepGraze
            ('jump', SheepJump),    # Link subcommand 'jump'  to class SheepJump
            # Add more subcommands here
            ]


if __name__ == '__main__':
    Sheep().digest()
</input>



When the above program is saved as file
``sheepactions.py`` and executed, we have:

<input content="shell">
sheepactions.py -h
</input>


The sub-commands ``graze`` and ``jump`` are clearly shown in
the help message.  In order to display their individual
usage one should pass any of these sub-commands followed by
the ``--help/-h`` switch. For example, to display the usage
for ``graze``:

<input content="shell">
sheepactions.py graze -h
</input>

..

  Example of execution: 
  
  In command line:
  
<input content="shell">
sheepactions.py graze -f daisies
sheepactions.py jump -n 5
</input>
  
  Equivalently, in Python interpreter:

<input content="python">
from sheepactions import *
SheepGraze()(feed='daisies')
SheepJump()(n=5)
</input>

.. _fullexample:

Attaching one node to another
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In addition to attaching functions to a node, it is also
possible to attach nodes to another node, as demonstrated by
lines 18 and 19 of the following example

<input content="python" save_as="sheepgame.py">
import argpext

import sheepactions # Module sheepactions is provided by previous example.



class FeedWolf(argpext.Task):
    "Feed the wolf"

    def hook(self,prey):
        print('Wolf eats %s' % prey)

    def populate(self,parser):
        parser.add_argument('-p', dest='prey', default='sheep', 
                            help='Specify the food. Default:"%(default)s".')

class Main(argpext.Node):
    "Top level sheepgame options"
    SUBS = [
        ('sheep', sheepactions.Sheep), # Attaching another Node
        ('feed-wolf', FeedWolf), # Attaching a Task
        # Add more subcommands here
        ]

if __name__ == '__main__':
    Main().digest()
</input>


This methodology allows one to build a rather general
hierarchical tree-like structure of subcommands of
non-uniform height.


.. _fullexample_usage:

When the above program is saved as file ``sheepgame.py``,
the top level help message is invoked as follows:

<input content="shell">
sheepgame.py -h
</input>


To display sheep-related usage of ``sheepgame.py``, 
pass the ``sheep`` subcommand:

<input content="shell">
sheepgame.py sheep -h
</input>

To display even lower level help messages, additional
sub-commands are passed:

<input content="shell">
sheepgame.py sheep jump -h
sheepgame.py sheep graze -h
</input>

..
  
  Examples of execution:

  In the command line:

<input content="shell">
sheepgame.py sheep jump -n 5
sheepgame.py sheep graze
sheepgame.py sheep graze -f daisies
</input>


  Equivalently, in Python interpreter:

<input content="python">
from sheepgame import sheepactions
sheepactions.SheepJump()(n=5)
sheepactions.SheepGraze()()
sheepactions.SheepGraze()(feed='daisies')
</input>


Wolf-related usage of ``sheepgame.py``:

<input content="shell">
sheepgame.py feed-wolf -h
</input>

.. _fullexample_execution:

..
  
  Example of execution:
  
  In the command line:

<input content="shell">
sheepgame.py feed-wolf
</input>

  Equivalently, in Python interpreter

<input content="python">
import sheepgame
sheepgame.FeedWolf()()
</input>
  


Tasks with multiple arguments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For simplicity, so far we have only considered functions of
one argument. In practice, there is no such limitation. 

For each argument of the function pointed to by the
:attr:`hook` attribute there should be a call to
:meth:`add_argument` inside :meth:`populate`, whose
``dest=`` value coincides with the name of the argument.

One should take full advantage of the rich set of options
provided :mod:`argparse` methods such as
:meth:`add_argument`.

Here is an example, where the three arguments ``quantity``,
``feed``, and ``hours`` correspond to the three
:meth:`add_argument` calls with ``dest='quantity'``,
``dest='feed'`` and ``dest='hours'``:

<input content="python" save_as="sheepgraze2.py">
import argpext

def sheep_graze(quantity,feed,hours):
    print( ('%s of sheep grazes on %s for %.1f hours.' \
              % (quantity, feed, hours) ).capitalize() )

class SheepGraze(argpext.Task):
    "Let sheep graze"
    hook = argpext.make_hook(sheep_graze)
    def populate(self,parser):
        parser.add_argument(dest='quantity', help='Quantity of sheep.')
        parser.add_argument('-f', dest='feed', default='grass', 
                            help='Specify the feed. Default: %(default)s.')
        parser.add_argument('-t', dest='hours', default=2.5, type=float,
                            help='Specify number of hours. Default: %(default)s.')

if __name__ == '__main__':
    SheepGraze().digest()
</input>

The usage is as follows:

<input content="shell">
sheepgraze2.py -h
</input>


..

  Execution examples

  In command line

<input content="shell">
sheepgraze2.py dosen
sheepgraze2.py herd -t 5
sheepgraze2.py herd -f hay
</input>


  Equivalently, in Python interpreter

<input content="python">
import sheepgraze2
sheepgraze2.SheepGraze()('dosen')
sheepgraze2.SheepGraze()('herd',hours=5)
sheepgraze2.SheepGraze()('herd',feed='hay')
</input>

  Notice the agreement between the default values
  (e.g. ``hour=2.5``) applied when an optional argument is
  missing in the command line examples and those in the
  corresponding Python interpreter examples.


Static :meth:`hook` methods
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Our :ref:`bare bones example<sheepgraze>` can be
equivalently rewritten in a different style, as follows

<input content="python">
import argpext

class SheepGraze(argpext.Task):
    "Let sheep graze"

    def hook(self,feed):
        print('Sheep grazes on %s' % feed)

    def populate(self,parser):
        parser.add_argument('-f', dest='feed', default='grass', 
                            help='Specify the feed. Default: %(default)s.')

if __name__ == '__main__':
    SheepGraze().digest()
</input>


Return values
^^^^^^^^^^^^^

The :meth:`Node.digest`, :meth:`Task.digest` and
:meth:`Task.__call__` methods return the value of the
corresponding reference function. For example:


<input content="python">
import argpext

def square(x=1):
    "Calculate the square of an argument"
    return x*x

class Square(argpext.Function):
    hook = argpext.make_hook(square)
    def populate(self,parser):
        parser.add_argument('-x', default=2, type=float,
                            help='Specify the value of x.')

y = Square().digest(prog=None,args=['-x','2'])
print( y )

y = Square()(x=4)
print( y )

y = Square()()
print( y )

y = Square()() # Todo: add custom execution
print( y )
</input>




Command line history log
^^^^^^^^^^^^^^^^^^^^^^^^

Commands managed by Argpext are optionally saved into a
local history. The feature is disabled by default; to enable
it, set the environment variable
:py:envvar:`ARGPEXT_HISTORY` to specify the name of the
history file. 

Command line history is available by running
:program:`argpext.py` as executable with ``history``
sub-command.


KeyWords variable type
-------------------------

This section introduces class :class:`KeyWords` to cover
the type of variables whose possible values (or methods for
generating those values) are known in advance; this is an
alternative to using the ``choices=`` argument of
:py:meth:`argparse.add_argument`.

Consider the following possible mnemonic choices for
specifying a date: "1977-02-04", "Lisas birthday", "y2kday",
"today", and their implementation:

<input content="python">
import argpext

from argpext import *
import time

def today():
    "Return todays date in YYYY-MM-DD representation"
    return time.strftime('%Y-%m-%d', time.localtime())

dates = KeyWords([
    '1977-02-04',
    'Lisas birthday',
    'y2kday',
    'today'
])



str(dates)

dates('1977-02-04')
dates('Lisas birthday') 
dates('y2kday') 
dates('today') # Function today() is implicitly invoked at this line.
dates('2012-01-11') # Value not predefined
</input>


The three predefined values of date are declared in lines
9-11; whereas line 12 declares a predefined method for
finding the value of date:

| *Line 9*: The value of the item is made identical to its reference key ``1977-02-04``.
| *Line 10*: The reference key is ``Lisas birthday``; the value is fixed and equal to ``1977-01-01``.
| *Line 11*: The reference key is ``y2kday``; the value is fixed and equal to ``2000-01-01``.
| *Line 12*: The reference key is ``today``; the value is computed by function :func:`today` at the time of the actual evaluation (line 21).

Actual evaluations are shown in lines 18-27.

The :class:`KeyWords` type object ``dates``, constructed
in the above example can be used as ``type=`` argument,
similar to the case in our next :ref:`example<sheepgraze3>`.


Treatment of unmatched values
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The last evaluation (line 26) results in an error because
the argument ``2012-01-11`` does not match any of predefined
values. 


.. _categ_example1:

The bare bones example revisited
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Going back to :ref:`one<sheepgraze>` of our previously
discussed examples :class:`KeyWords` type values may be
found particularly useful. Problems may arise because
:ref:`command line usage<sheepgraze_usage>` for that example
allows one to pass any erroneous string as an
argument. Indeed, consider this:

.. _categ_example1_program:

<command>
sheepgraze.py -f money
</command>


The :class:`KeyWords` class allows one to limit the
domain of argument values to a limited set of valid values
and reflect the available choices in the usage. Introducing
the :class:`KeyWords` class into our example leads to the
following:

.. _sheepgraze3:

<input content="python" save_as="sheepgraze3.py">
import argpext

def sheep_graze(feed):
    print('Sheep grazes on %s' % feed)


class SheepGraze(argpext.Task):
    "Let sheep graze"

    hook = argpext.make_hook(sheep_graze)

    def populate(self,parser):
        parser.add_argument('-f', dest='feed', default='grass'
                            , type=argpext.KeyWords(['hay',
                                                     'grass',
                                                     'daisies'])
                            , help='Specify the feed. '\
                                'Choose from: %(type)s. '\
                                'Default: %(default)s.')

if __name__ == '__main__':
    SheepGraze().digest()
</input>
   :lines: 3-
   :emphasize-lines: 12-14,16
   :linenos:

The highlighted lines (12-14, and 16) emphasize changes relative to the
:ref:`original program<sheepgraze>`.

After this modification, the valid values (``hay``,
``grass``, and ``daisies``) of input become visible within
the help message. Indeed:

<input content="shell">
sheepgraze3.py -h
</input>

..
  
  Examples of execution:

  Passing any of the valid values results in proper execution:
  
<input content="shell">
sheepgraze3.py -f hay
sheepgraze3.py -f daisies
</input>

  Attempt to pass an erroneous argument leads to an
  error message:
  
<input content="shell">
sheepgraze3.py -f money
</input>


.. _argpext_exe:

Argpext as an executable
------------------------

In addition to providing a Python module, program
:program:`argpext.py` can be ran as an executable; its
current usage is as follows:

<input content="shell">
argpext -h
</input>

.. _reference:

Reference
-----------------------------------------


Sub-command hierarchy
^^^^^^^^^^^^^^^^^^^^^

.. class:: Task

   Base class for a callable function-like object that is
   capable of behaving like a script.  The object can be
   evaluated in two ways. As a script-like object, it can be
   evaluated on a sequence of command line arguments, using
   method :meth:`digest`. As function-like object it can be
   evaluated directly, using the function call operator; See
   method :meth:`__call__` for details. The object is
   attached to a regular Python function (also called the
   *reference function*) by the :meth:`hook` method.

   .. staticmethod:: Task.hook(*args,**kwds)

	Specifies the reference Python function. If
	:meth:`hook` takes positive number of arguments,
	:meth:`Task.populate` must be properly
	overloaded as well.

   .. method:: Task.populate(parser)

	This method should be overloaded if :meth:`hook`
	takes positive number of arguments. For each argument *X* of
	the :meth:`hook` method there must be a call (or its
	equivalent) to :py:meth:`add_argument` with *dest='X'*.
        The *parser* argument should be assumed  to be of type
	:py:class:`argparse.ArgumentParser`.




   .. method:: Task.__call__(*args,**kwds)

	Execute the reference function; its return value is
	returned. The arguments of the reference function
	are given by *args* and *kwds*. If an argument of is
	missing, the command line default values, defined
	:meth:`Task.populate` are substituted. Notice
	that the default values, if any, defined in the
	arguments of :meth:`Task.hook` are not used. If
	too many arguments are given or some arguments
	remain missing, a standard built-in exception is
	raised.

   .. method:: Task.digest(prog=None,args=None)

	Execute the reference function; its return value is
	returned.  Task :meth:`Task.populate` is
	used to convert command line arguments given by
	*args* into the arguments of the reference
	function. Using the default value *args=None* is
	equivalent to setting *args=sys.argv[1:]*. The
	*prog* argument is the program name that appears in
	the command line help message when invoked. Using
	the default value *prog=None* is equivaent to
	setting *prog=sys.argv[0]*.

.. class:: Node

   Base class for hierarchical script-like object that can
   be executed on a complete list of command line
   arguments. The list starts with the mandatory sequence of
   sub-commands that identifies the leaf :func:`Task`
   class. The rest of the command line arguments are used to
   execute the reference function of that class, as
   specified in the documentation for
   :meth:`Task.digest` method.


   .. attribute:: SUBS

      Specifies the list of child nodes along with their
      assigned sub-commands. This attribute, if defined,
      must be a :py:class:`list` or a :py:class:`tuple`
      of *(key,basenode)* items, where the *basenode* is an
      instance of either of :class:`Node` or
      :class:`Task` class, and the *key* is the
      sub-command assigned to it.

   .. method:: Node.digest(prog=None,args=None)

      Execute the node based the sequence of sub-commands
      given by *args*. If *args=None*, it is automatically
      reassigned to `sys.argv[1:]`. Returns the value
      returned by the reference function corresponding to
      the sequence of sub-commands given by *args*.

      The *prog* argument is the program name that appears
      in the command line help message when invoked, the
      default value *None* translates to *sys.argv[0]*.


KeyWords variable type
^^^^^^^^^^^^^^^^^^^^^

.. class:: KeyWords(keywords=[])

   KeyWords variable type. A callable object that
   converts input key into itself, if one is defined,
   throwing a :py:exc:`KeyError` exception otherwise

   * keywords - a list-like object *[item1,item2,...]*, that defined ordered sequence of unique keys

   KeyWords variable type.

   .. method:: KeyWords.__str__()

      Returns string representation for the object showing
      all the available keys.

   .. method:: KeyWords.__call__(key)

      Returns the *key* itself, if *key* matches any of keys defined
      by the *keywords*. Otherwise, raises the
      :py:exc:`KeyError` exception.

Environment variables
^^^^^^^^^^^^^^^^^^^^^


.. envvar:: ARGPEXT_HISTORY

   Sub-command history file path. No history file is written
   if this variable is unset.



Porting from the earlier Argpext versions
-----------------------------------------

Compared to the previous releases (0.1 and 0.2) of argpext,
version 1.0 is a very substantial update. For consistency
with the "Style Guide for Python Code" (PEP 8), class
:class:`comm_cls` is renamed into :class:`Task` and
class :class:`node_cls` is renamed into :class:`Node`.
Class :class:`keyval` is renamed into
:class:`KeyWords`. Interface to those classes have also
been changed.  

Version 1.1 is a bugfix version that addresses minor issues.

Version 1.2 introduces introduces multiple new features.

See also
--------

* `Argparse Sub-commands <http://docs.python.org/py3k/library/argparse.html#sub-commands>`_

* http://pypi.python.org/pypi/Baker

* https://github.com/anandology/subcommand


Contents:
----------------------------------

.. toctree::
   :maxdepth: 2



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

