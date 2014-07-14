###################################
Argpext |release| --- Documentation
###################################

.. package:: argpext

:py:mod:`argpext` is a Python package, originally designed, developed and maintained by Alex Shirokov since 2012.

Argpext provides hierarchical, or multilevel, subcommand
implementation that allows one to quickly expose any required callable
objects, such as functions, generators, to a DOS/Linux command line.


###################################
Command line linking utilities
###################################

.. _task:

``Task`` class
============================

We start with two full-featured examples on how to link a standalone
function or generator to the *SHELL* command line interface.

Example: linking a standalone function to command line
----------------------------


In this example, a function *f(m,n)* takes integer arguments *m* and
*n*.

Our objective is to link this function to the command line
interface. 

We require that using the command line alone we should be able to:

* See the help message documenting the usage of command line interface 

* Specify the arguments required by the function

* Execute the function based on the value of argument we have specified

* See the string representation of the value returned by *f(m,n)*

In addition, we should be able to access the full-featured value
returned by function *f(m,n)* in Python.

The above requirements are implemented in the code below.  


.. note:: Code description: we wish to define command line interface
  for the standalone function *f(m,n)*. To link function *f(m,n)* to
  the command line, we define class *F*, an instance of ``Task``, as
  follows. By defining its *hook* member, we establish the linkage
  between class *F* and function *f*; by defining its *populate*
  member we specify how to populate function's arguments based on the
  command line inputs. This function requires the command line
  *parser* as argument. The *parser* argument should be treated as
  variable of the ``argparse.ArgumentParser`` type; as such, the
  parser should be populated exactly as described documentation for
  the standard Python's *argparse* module. In our case, it is
  populated by a sequence of ``parser.add_argument( ... )`` calls: one
  call for each argument.


.. _e3:
<input directory="examples" read="e3.py" content="python" action="show" flags="show_filename"/>


Here, ``s2m`` is used to convert the standalone function *f* into the
bound ``hook`` method, required any instance of the ``Task`` class.

Also, expression ``customize(tostring=str)`` is used to indicate our
requirement that the default string representation of the return value
of *f(m,n)* appears within the command line output.

To suppress the appearance of the return value of *f(m,n)* in command
line output, use ``hook = customize(tostring=None)(s2m( f ))``,
alternatively use ``hook = customize()(s2m( f ))``, or simply ``hook =
s2m( f )``; function *f(m,n)* will still be executed.

To test the implementation, we execute from the *SHELL*:

<input directory="examples" content="shell" action="execute">
python e3.py --help

python e3.py 2

python e3.py 2 -n 5
</input>

Equivalently, we execute in *Python*:

<input directory="examples" content="python" action="execute">
import e3
e3.F().sdigest('-h')

a = e3.F().sdigest('2')
print(a)

a = e3.F().sdigest('2 -n 5')
print(a)
</input>

Specifying argument items explicitly

<input directory="examples" content="python" action="execute">
import e3
a = e3.F().sdigest(['2', '-n', '5'])
print(a)
</input>




Example: linking a standalone generator to command line
----------------------------

In this example, a standalone generator *g(m,n)* takes integer
arguments *m* and *n*.

Our objective is to link this generator to the command line interface.

We require that using the command line alone we should be able to:

* See the help message documenting the usage of command line interface 

* Specify the arguments required by the function

* Execute the function based on the value of argument we have specified

* See the string representations of the values yielded by the
  generator immediately as they get provided.

In addition, we should be able to access the full-featured values
yielded by the generator *g(m,n)* in the Python session, immediately
as they get provided.


The above requirements are implemented as follows

.. _e1:
<input directory="examples" read="e1.py" content="python" action="show" flags="show_filename"/>

To test the implementation, we execute from the *SHELL*:

<input directory="examples" content="shell" action="execute">
python e1.py --help

python e1.py 2

python e1.py 2 -n 5
</input>

We execute in *Python*:

<input directory="examples" content="python" action="execute">
import e1
e1.G().sdigest('-h')

for a in e1.G().sdigest('2'):
    print(a)

for a in e1.G().sdigest('2 -n 5'):
    print(a)
</input>






Creating ``hook`` as pure bound method
----------------------------

In order to link a code body to the command line it is not required to
have it encapsulated within a standalone function. The following shows
an example identical to the :ref:`example<e3>` shown above, except
that the body of the function *f(m,n)* is now embedded within the
definition of the ``hook`` method, inside class *F* declaration,
rather than being a standalone task method:

<input directory="examples" read="e4.py" content="python" action="show" flags="show_filename"/>

<input directory="examples" content="shell" action="test-execute">
python e4.py --help

python e4.py 2 -n 5
</input>

<input directory="examples" content="python" action="test-execute">
import e4
b = e4.F().sdigest('2 -n 5')
for a in b:
    print(a)
</input>

Return value display: options and customization
----------------------------

Return value display can be disable, enabled or customized.

In order to disable the return value display, simply use
``@customize(tostring=None)``, or ``@customize()``, or avoid using the
``@customize`` decorator alltogether, as in the following example

<input directory="examples" read="a1.py" content="python" action="show" flags="show_filename"/>

<input directory="examples" read="a3.py" content="python" action="show" flags="show_filename"/>

<input directory="examples" content="shell" action="test-execute">
python a1.py --help
python a1.py
</input>

<input directory="examples" content="python" action="test-execute">
import a1
b = a1.C().sdigest(display=True)
for a in b:
    print( a )
</input>


Customized display of function return value


<input directory="examples" content="shell" action="execute">
python a3.py
</input>

<input directory="examples" content="shell" action="execute">
python a4.py
</input>


<input directory="examples" content="python" action="execute">
import a3
b = a3.C().sdigest(display=True)
b
</input>

It is possible to redirect the output into a customized stream; for
example

<input directory="examples" content="python" action="execute">
import io
stream = io.StringIO()

import a3
b = a3.C().sdigest(stream=stream,display=True)
stream.getvalue()
b
</input>


Customized display of values provided by task generator

<input directory="examples" read="a4.py" content="python" action="show" flags="show_filename"/>

<input directory="examples" content="python" action="execute">
import a4
b = a4.C().sdigest(display=True)
for a in b:
    print( a )
</input>





*Node* class
==================

In :ref:`previous section<task>` we presented multiple examples of
linking Python code to command line interface. As the number of tasks
grows it becomes more and more difficult for the developer to keep
track of them, especially if there is an implicit relation between
the tasks.

This section presents the *Node* class, -- a tool that allows you to
integrate all the related tasks into a single *master* script, by
organizing them elegantly into a *task tree* structure.


Building the first level of hierarchy
----------------------------

For example, we can quickly organize all the tasks we have defined in
:ref:`previous section<task>` within a single script *n1.py* as
follows:

<input directory="examples" read="n1.py" content="python" action="show" flags="show_filename"/>

The *master* script, when executed with the ``--help/-h`` flag,
produces the *master help message*, as follows:

<input directory="examples" content="shell" action="execute">
python n1.py -h
</input>

<input directory="examples" content="python" action="execute">
import n1
n1.Main().sdigest('-h')
</input>

The positional arguments shown above indicate the list of all tasks
available. By passing one of them as an additional positional argument
to the master script, we descend to the level of the specific task
selected for the execution. In this manner we can execute any of the
available tasks.


Example: executing sub-task e3
^^^^^^^^^^^^^^^^^^^^

For example, when selecting task *e3* for execution, we must populate
the arguments required by the task, which is done by first retrieving
help message as follows:

<input directory="examples" content="shell" action="execute">
python n1.py e3 -h
</input>
<input directory="examples" content="python" action="execute">
import n1
n1.Main().sdigest('e3 -h')
</input>


Having reviewed all the options available for executing the task, we
populate task arguments according to the usage and execute the task
twice (once with *m=2,n=3*, and once with *m=3,n=5*) as follows


<input directory="examples" content="shell" action="execute">
python n1.py e3 2
python n1.py e3 2 -n 5
</input>
<input directory="examples" content="python" action="execute">
import n1
n1.Main().sdigest('e3 2')
n1.Main().sdigest('e3 2 -n 5')
</input>



Example: executing sub-task a4
^^^^^^^^^^^^^^^^^^^^


Similarly, we may choose to execute task *a4*. The help message for is
generated as follows:

<input directory="examples" content="shell" action="execute">
python n1.py a4 -h
</input>

<input directory="examples" content="python" action="execute">
import n1
n1.Main().sdigest('a4 -h')
</input>



We recall from the :ref:`section<task>` describing the task class,
that task *a4* structurally differs from task *e3* in that the former
starts an iterator, whereas the latter executes a serial task. Using
the master script, task *a4* is executed as follows


<input directory="examples" content="shell" action="execute">
python n1.py a4
</input>

<input directory="examples" content="python" action="execute">
import n1
for element in n1.Main().sdigest('a4',display=True):
    print( element )
</input>


The objective of the *Node* class is achieved: as we have demonstrated
with the examples above each task is accessible by passing command
line arguments to the master script only.






###############################
Contents:
###############################

.. toctree::
   :maxdepth: 2

###############################
Indices and tables
###############################


* :ref:`genindex`  
* :ref:`modindex`
* :ref:`search`

