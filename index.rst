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

.. literalinclude:: examples/sheepgraze0.py
   :language: python3
   :lines: 3-


The identical functionality is now achieved with our Argpext as follows:

.. _sheepgraze:

.. literalinclude:: examples/sheepgraze.py
   :language: python3
   :lines: 3-

Class :class:`SheepGraze`, constructed by inheritance from
:class:`argpext.Function`, establishes the interface between
command line and function :func:`sheep_graze`.

Command line is processed during the call to the
:meth:`SheepGraze.digest` function.

The docstring ``"Let sheep graze"`` shows up inside the
usage. Indeed, when the above program is saved as file
``sheepgraze.py`` and executed with the ``--help`` or ``-h``
switches, we have:

.. _sheepgraze_usage:

.. literalinclude:: examples/sheepgraze_help.tmp

..
  
  Examples of execution

  Function :func:`sheep_graze` can be executed from the
  command line as follows:
  
  .. literalinclude:: examples/sheepgraze.tmp
  .. literalinclude:: examples/sheepgraze_daisies.tmp

  Equivalently, in Python interpreter:

  .. literalinclude:: examples/sheepgraze_cmd.tmp
  .. literalinclude:: examples/sheepgraze_daisies_cmd.tmp



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
in the example below. Functions :func:`SheepGraze` and
:func:`SheepJump` are now attached to node :class:`Sheep`.

The next key thing is to include :meth:`Sheep.digest()` at
the bottom in order to execute command line on our new
interface.


.. _sheepactions:
.. literalinclude:: examples/sheepactions.py
   :language: python3
   :lines: 3-

When the above program is saved as file
``sheepactions.py`` and executed, we have:

.. literalinclude:: examples/sheepactions_help.tmp

The sub-commands ``graze`` and ``jump`` are clearly shown in
the help message.  In order to display their individual
usage one should pass any of these sub-commands followed by
the ``--help/-h`` switch. For example, to display the usage
for ``graze``:

.. literalinclude:: examples/sheepactions_graze_help.tmp

..

  Example of execution: 
  
  In command line:
  
  .. literalinclude:: examples/sheepactions_graze_daisies.tmp
  .. literalinclude:: examples/sheepactions_jump_j5.tmp
  
  Equivalently, in Python interpreter:

  .. literalinclude:: examples/sheepactions_graze_daisies_cmd.tmp
  .. literalinclude:: examples/sheepactions_jump_j5_cmd.tmp



.. _fullexample:

Attaching one node to another
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In addition to attaching functions to a node, it is also
possible to attach nodes to another node, as demonstrated by
lines 18 and 19 of the following example

.. literalinclude:: examples/sheepgame.py
   :language: python3
   :lines: 3-
   :linenos:

This methodology allows one to build a rather general
hierarchical tree-like structure of subcommands of
non-uniform height.


.. _fullexample_usage:

When the above program is saved as file ``sheepgame.py``,
the top level help message is invoked as follows:

.. literalinclude:: examples/sheepgame_help.tmp


To display sheep-related usage of ``sheepgame.py``, 
pass the ``sheep`` subcommand:

.. literalinclude:: examples/sheepgame_sheep_help.tmp

To display even lower level help messages, additional
sub-commands are passed:

.. literalinclude:: examples/sheepgame_sheep_jump_help.tmp


.. literalinclude:: examples/sheepgame_sheep_graze_help.tmp

..
  
  Examples of execution:

  In the command line:

  .. literalinclude:: examples/sheepgame_sheep_jump5.tmp
  .. literalinclude:: examples/sheepgame_sheep_graze.tmp
  .. literalinclude:: examples/sheepgame_sheep_graze_daisies.tmp

  Equivalently, in Python interpreter:

  .. literalinclude:: examples/sheepgame_sheep_jump5_cmd.tmp
  .. literalinclude:: examples/sheepgame_sheep_graze_cmd.tmp
  .. literalinclude:: examples/sheepgame_sheep_graze_daisies_cmd.tmp
  

Wolf-related usage of ``sheepgame.py``:

.. literalinclude:: examples/sheepgame_wolf_help.tmp

.. _fullexample_execution:

..
  
  Example of execution:
  
  In the command line:

  .. literalinclude:: examples/sheepgame_wolf_feed.tmp

  Equivalently, in Python interpreter

  .. literalinclude:: examples/sheepgame_wolf_feed_cmd.tmp
  


Functions with multiple arguments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For simplicity, so far we have only considered functions of
one argument. In practice, there is no such limitation. 

For each argument of the function pointed to by the
:attr:`HOOK` attribute there should be a call to
:meth:`add_argument` inside :meth:`populate`, whose
``dest=`` value coincides with the name of the argument.

One should take full advantage of the rich set of options
provided :mod:`argparse` methods such as
:meth:`add_argument`.

Here is an example, where the three arguments ``quantity``,
``feed``, and ``hours`` correspond to the three
:meth:`add_argument` calls with ``dest='quantity'``,
``dest='feed'`` and ``dest='hours'``:

.. literalinclude:: examples/sheepgraze2.py
   :language: python3
   :lines: 3-

The usage is as follows:

.. literalinclude:: examples/sheepgraze2_help.tmp

..

  Execution examples

  In command line

  .. literalinclude:: examples/sheepgraze2_exe1.tmp
  .. literalinclude:: examples/sheepgraze2_exe2.tmp
  .. literalinclude:: examples/sheepgraze2_exe3.tmp

  Equivalently, in Python interpreter

  .. literalinclude:: examples/sheepgraze2_exe1_cmd.tmp
  .. literalinclude:: examples/sheepgraze2_exe2_cmd.tmp
  .. literalinclude:: examples/sheepgraze2_exe3_cmd.tmp

  Notice the agreement between the default values
  (e.g. ``hour=2.5``) applied when an optional argument is
  missing in the command line examples and those in the
  corresponding Python interpreter examples.


Static :meth:`HOOK` methods
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Our :ref:`bare bones example<sheepgraze>` can be
equivalently rewritten in a different style, as follows

.. literalinclude:: examples/sheepgraze_hook.py
  :lines: 3-

Return values
^^^^^^^^^^^^^

The :meth:`Node.digest`, :meth:`Function.digest` and
:meth:`Function.__call__` methods return the value of the
corresponding reference function. For example:

.. literalinclude:: examples/retval.tmp
  :lines: 3-



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


Categorical variable type
-------------------------

This section introduces class :class:`Categorical` to cover
the type of variables whose possible values (or methods for
generating those values) are known in advance; this is an
alternative to using the ``choices=`` argument of
:py:meth:`argparse.add_argument`.

Consider the following possible mnemonic choices for
specifying a date: "1977-02-04", "Lisas birthday", "y2kday",
"today", and their implementation:

.. literalinclude:: examples/categdate.tmp
   :linenos:
   :lines: 3-

The three predefined values of date are declared in lines
9-11; whereas line 12 declares a predefined method for
finding the value of date:

| *Line 9*: The value of the item is made identical to its reference key ``1977-02-04``.
| *Line 10*: The reference key is ``Lisas birthday``; the value is fixed and equal to ``1977-01-01``.
| *Line 11*: The reference key is ``y2kday``; the value is fixed and equal to ``2000-01-01``.
| *Line 12*: The reference key is ``today``; the value is computed by function :func:`today` at the time of the actual evaluation (line 21).

Actual evaluations are shown in lines 18-27.

The :class:`Categorical` type object ``dates``, constructed
in the above example can be used as ``type=`` argument,
similar to the case in our next :ref:`example<sheepgraze3>`.


Treatment of unmatched values
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The last evaluation (line 26) results in an error because
the argument ``2012-01-11`` does not match any of predefined
values. This error behaviour may be changed by passing an
additional ``typeothers=`` argument to the constructor of
:class:`Categorical`. Setting ``typeothers=str`` for example
will result in the conversion of any unmatched values to
string (:class:`str`).


.. _categ_example1:

The bare bones example revisited
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Going back to :ref:`one<sheepgraze>` of our previously
discussed examples :class:`Categorical` type values may be
found particularly useful. Problems may arise because
:ref:`command line usage<sheepgraze_usage>` for that example
allows one to pass any erroneous string as an
argument. Indeed, consider this:

.. _categ_example1_program:

.. literalinclude:: examples/sheepgraze_money.tmp


The :class:`Categorical` class allows one to limit the
domain of argument values to a limited set of valid values
and reflect the available choices in the usage. Introducing
the :class:`Categorical` class into our example leads to the
following:

.. _sheepgraze3:

.. literalinclude:: examples/sheepgraze3.py
   :lines: 3-
   :emphasize-lines: 12-14,16
   :linenos:

The highlighted lines (12-14, and 16) emphasize changes relative to the
:ref:`original program<sheepgraze>`.

After this modification, the valid values (``hay``,
``grass``, and ``daisies``) of input become visible within
the help message. Indeed:

.. literalinclude:: examples/sheepgraze3_help.tmp

..
  
  Examples of execution:

  Passing any of the valid values results in proper execution:
  
  .. literalinclude:: examples/sheepgraze3_hay.tmp
  .. literalinclude:: examples/sheepgraze3_daisies.tmp

  Attempt to pass an erroneous argument leads to an
  error message:
  
  .. literalinclude:: examples/sheepgraze3_money.tmp


.. _argpext_exe:

Argpext as an executable
------------------------

In addition to providing a Python module, program
:program:`argpext.py` can be ran as an executable; its
current usage is as follows:

.. literalinclude:: examples/argpext_help.tmp


.. _reference:

Reference
-----------------------------------------


Sub-command hierarchy
^^^^^^^^^^^^^^^^^^^^^

.. class:: Function

   Base class for a callable function-like object that is
   capable of behaving like a script.  The object can be
   evaluated in two ways. As a script-like object, it can be
   evaluated on a sequence of command line arguments, using
   method :meth:`digest`. As function-like object it can be
   evaluated directly, using the function call operator; See
   method :meth:`__call__` for details. The object is
   attached to a regular Python function (also called the
   *reference function*) by the :meth:`HOOK` method.

   .. staticmethod:: Function.HOOK(*args,**kwds)

	Specifies the reference Python function. If
	:meth:`HOOK` takes positive number of arguments,
	:meth:`Function.populate` must be properly
	overloaded as well.

   .. method:: Function.populate(parser)

	This method should be overloaded if :meth:`HOOK`
	takes positive number of arguments. For each argument *X* of
	the :meth:`HOOK` method there must be a call (or its
	equivalent) to :py:meth:`add_argument` with *dest='X'*.
        The *parser* argument should be assumed  to be of type
	:py:class:`argparse.ArgumentParser`.




   .. method:: Function.__call__(*args,**kwds)

	Execute the reference function; its return value is
	returned. The arguments of the reference function
	are given by *args* and *kwds*. If an argument of is
	missing, the command line default values, defined
	:meth:`Function.populate` are substituted. Notice
	that the default values, if any, defined in the
	arguments of :meth:`Function.HOOK` are not used. If
	too many arguments are given or some arguments
	remain missing, a standard built-in exception is
	raised.

   .. method:: Function.digest(prog=None,args=None)

	Execute the reference function; its return value is
	returned.  Function :meth:`Function.populate` is
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
   sub-commands that identifies the leaf :func:`Function`
   class. The rest of the command line arguments are used to
   execute the reference function of that class, as
   specified in the documentation for
   :meth:`Function.digest` method.


   .. attribute:: SUBS

      Specifies the list of child nodes along with their
      assigned sub-commands. This attribute must be defined
      and must be a :py:class:`list` or a :py:class:`tuple`
      of *(key,basenode)* items, where the *basenode* is an
      instance of either of :class:`Node` or
      :class:`Function` class, and the *key* is the
      sub-command assigned to it.
      :py:exc:`InitializationError` is raised if this
      attribute is not defined at the evaluation time.

   .. method:: Node.digest(prog=None,args=None)

      Execute the node based the sequence of sub-commands
      given by *args*. If *args=None*, it is automatically
      reassigned to `sys.argv[1:]`. Returns the value
      returned by the reference function corresponding to
      the sequence of sub-commands given by *args*.

      The *prog* argument is the program name that appears
      in the command line help message when invoked, the
      default value *None* translates to *sys.argv[0]*.


Categorical variables
^^^^^^^^^^^^^^^^^^^^^

.. class:: Categorical(mapping=(),typeothers=None)

   Categorical variable type. A callable object that
   converts input key into its corresponding literal value,
   computing the latter if necessary.

   * mapping - this argument should be a list-like object *[item1,item2,...]*, needed to set up the mapping between the *the key*\s and *value*\s that correspond to each of those *key*\s. Each *item* can be one of the following:

     * [*key*, *unit*] - where *value* is an instance of type :class:`Unit`.

     * [*key*, *value*] - where *value* is an instance of any other type. This item is equivalent to [*key*, :class:`Unit`\(value= *value*\)]

     * *key* - equivalent to item  [*key*, :class:`Unit`\(value= *key*\) ]

     :py:exc:`InitializationError` exception is raised if *mapping* is not properly defined.

   * typeothers - Specifies the behavior when value for an undefined key is requested; See :meth:`Categorical.__call__` for details.

   Categorical variable type.

   .. method:: Categorical.__str__()

      Returns string representation for the object showing
      all the available keys.

   .. method:: Categorical.__call__(key)

      Finds and returns the literal value associated with
      the given *key*.  If *key* does not match any of keys
      defined by the *mapping* then *typeothers(key)* is
      returned, unless *typeothers* is *None* (the default)
      in which case :py:exc:`KeyEvaluationError` exception
      is raised.

.. class:: Unit(value,help=None,callable=False)

   Value unit for :class:`Categorical` variables. The
   instance of this class completely specifies how the value
   should be computed when it is requested.

   .. method:: Unit.evaluate()

     Returns the literal value of valuation unit. When the
     *callable* argument to :class:`Unit` is *False*, it is
     identical to its *value* argument. When
     *callable=True*, the literal value is found by
     evaluation of *value()* at the time when the
     :meth:`evaluate` is invoked.


Exceptions
^^^^^^^^^^

   .. exception:: InitializationError

   .. exception:: KeyEvaluationError



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
:class:`comm_cls` is renamed into :class:`Function` and
class :class:`node_cls` is renamed into :class:`Node`.
Class :class:`keyval` is renamed into
:class:`Categorical`. Interface to those classes have also
been changed.  

Version 1.1 is a bugfix version that addresses minor issues.

Version 2.0 is a significant improvement.

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

