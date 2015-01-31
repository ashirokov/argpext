###################################
Argpext |release| --- Documentation
###################################


###################################
Hierarchical command line interface
###################################

Hierarchical command line interface utility of the ``argpext`` package
aims to provide very efficient bindings between callable python
objects, such as functions, or generators to the command
line. Implementation proceeds through two primary components: the
``Task`` and ``Node`` classes.

.. _task:

Linking a standalone function to command line
============================

In this example, a function *f(m,n)* takes integer arguments *m* and
*n*.

Our objective is to link this function to the command line
interface, so we can execute it from DOS/Unix and Python
command prompt.

We require that using the command line alone we should be able to:

* See the help message documenting the usage of command line interface 

* Specify the arguments required by the function

* Execute the function based on the value of argument we have specified

* See the string representation of the value returned by *f(m,n)*

In addition, we should be able to access the full-featured value
returned by function *f(m,n)* in Python.

The above requirements are implemented in the code below.  


.. _a:
<input directory="examples" read="a.py" content="python" action="show" flags="show_filename"/>

To link function *f(m,n)* to the command line, we define class *T*, an
instance of ``Task``, as follows. 

By defining its *hook* member, we establish the linkage between class
*T* and function *f*. 

The ``s2m`` function converts the standalone function *f* into the
bound class method.

Expression ``customize(tostring=str)`` indicates that we wish to see
string representation of the return value of function *f(m,n)* to
appear within the command line output. Without this ``customize``
call, the return value will not be displayed.

By defining its *populate* member we specify how to
populate function's arguments based on the command line inputs. This
function requires the command line *parser* as argument. The
*parser* argument should be treated as variable of the
``argparse.ArgumentParser`` type; as such, the parser should be
populated exactly as described documentation for the standard
Python's *argparse* module. In our case, it is populated by a
sequence of ``parser.add_argument( ... )`` calls: one call for each
argument.

Help messages on usage are displayed by using the ``-h/--help`` flag

<input directory="examples" content="shell" action="execute">
python a.py --help
</input>

Help messages are also available using the same flag, from the Python
command line prompt:

<input directory="examples" content="python" action="execute">
import a
a.T().sdigest('-h')
</input>





To test the implementation, we execute from the DOS/Unix command prompt:

<input directory="examples" content="shell" action="execute">
python a.py 2
python a.py 2 -n 5
</input>

Equivalently, we execute in Python prompt:

<input directory="examples" content="python" action="execute">
import a
a.T().sdigest('2')
a.T().sdigest('2 -n 5')
</input>

It is possible to specify argument items explicitly by passing a list of items as argument

<input directory="examples" content="python" action="execute">
import a
x = a.T().sdigest(['2', '-n', '5'])
print( x )
</input>




Linking a standalone generator to command line
============================


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

.. _b:
<input directory="examples" read="b.py" content="python" action="show" flags="show_filename"/>

To test the implementation, we execute from the *SHELL*:

<input directory="examples" content="shell" action="execute">
python b.py --help

python b.py 2

python b.py 2 -n 5
</input>

We execute in *Python*:

<input directory="examples" content="python" action="execute">
import b
b.T().sdigest('-h')

for x in b.T().sdigest('2'):
    print( x )

for x in b.T().sdigest('2 -n 5'):
    print( x )
</input>



Linking a bound method to command line
============================


In order to link a code body to the command line it is not required to
have it encapsulated within a standalone function. The following shows
an example identical to the :ref:`example<a>` shown above, except
that the body of the function *f(m,n)* is now embedded within the
definition of the ``hook`` method, inside class *F* declaration,
rather than being a standalone task method:

<input directory="examples" read="c.py" content="python" action="show" flags="show_filename"/>

<input directory="examples" content="shell" action="test-execute">
python c.py --help

python c.py 2 -n 5
</input>

<input directory="examples" content="python" action="test-execute">
import c
gn = c.T().sdigest('2 -n 5')
for x in gn:
    print(a)
</input>

Return value display: options and customization
============================

Return value display can be disable, enabled or customized.

In order to disable the return value display, simply use
``@customize(tostring=None)``, or ``@customize()``, or avoid using the
``@customize`` decorator alltogether, as in the following example

<input directory="examples" read="d.py" content="python" action="show" flags="show_filename"/>

<input directory="examples" read="e.py" content="python" action="show" flags="show_filename"/>

<input directory="examples" content="shell" action="test-execute">
python d.py --help
python d.py
</input>

<input directory="examples" content="python" action="test-execute">
import d
gn = d.T().sdigest(display=True)
for x in gn:
    print( x )
</input>


Customized display of function return value


<input directory="examples" content="shell" action="execute">
python e.py
</input>

<input directory="examples" content="python" action="execute">
import e
x = e.T().sdigest(display=True)
x
</input>

It is possible to redirect the output into a customized stream; for
example

<input directory="examples" content="python" action="execute">
import io
stream = io.StringIO()

import e
x = e.T().sdigest(stream=stream,display=True)
stream.getvalue()
x
</input>


Customized display of values provided by task generator

<input directory="examples" read="f.py" content="python" action="show" flags="show_filename"/>

<input directory="examples" content="shell" action="execute">
python f.py
</input>


<input directory="examples" content="python" action="execute">
import f
gn = f.T().sdigest(display=True)
for x in gn:
    print( x )
</input>





Building the first level of hierarchy
==================

In previous sections we presented multiple examples of linking Python
code to command line interface. As the number of tasks grows it
becomes more and more difficult for the developer to keep track of
them, especially if there is an implicit relation between the tasks.

This section presents the *Node* class, -- a tool that allows you to
integrate all the related tasks into a single *master* script, by
organizing them elegantly into a *task tree* structure.


For example, we can quickly organize all the tasks we have defined in
:ref:`previous section<task>` within a single script *n.py* as
follows:

<input directory="examples" read="n.py" content="python" action="show" flags="show_filename"/>

The *master* script, when executed with the ``--help/-h`` flag,
produces the *master help message*, as follows:

<input directory="examples" content="shell" action="execute">
python n.py -h
</input>

<input directory="examples" content="python" action="execute">
import n
n.T().sdigest('-h')
</input>

The positional arguments shown above indicate the list of all tasks
available. By passing one of them as an additional positional argument
to the master script, we descend to the level of the specific task
selected for the execution. In this manner we can execute any of the
available tasks.


For example, when selecting task *a* for execution, we must populate
the arguments required by the task, which is done by first retrieving
help message as follows:

<input directory="examples" content="shell" action="execute">
python n.py a -h
</input>
<input directory="examples" content="python" action="execute">
import n
n.T().sdigest('a -h')
</input>


Having reviewed all the options available for executing the task, we
populate task arguments according to the usage and execute the task
twice (once with *m=2,n=3*, and once with *m=3,n=5*) as follows


<input directory="examples" content="shell" action="execute">
python n.py a 2
python n.py a 2 -n 5
</input>
<input directory="examples" content="python" action="execute">
import n
n.T().sdigest('a 2')
n.T().sdigest('a 2 -n 5')
</input>



Similarly, we may choose to execute task *f*. The help message for is
generated as follows:

<input directory="examples" content="shell" action="execute">
python n.py f -h
</input>

<input directory="examples" content="python" action="execute">
import n
n.T().sdigest('f -h')
</input>



We recall from the :ref:`section<task>` describing the task class,
that task *f* structurally differs from task *e* in that the former
starts an iterator, whereas the latter executes a serial task. Using
the master script, task *f* is executed as follows


<input directory="examples" content="shell" action="execute">
python n.py f
</input>

<input directory="examples" content="python" action="execute">
import n
for x in n.T().sdigest('f',display=True):
    print('Also printing here:', x )
</input>


The objective of the *Node* class is achieved: as we have demonstrated
with the examples above each task is accessible by passing command
line arguments to the master script only.


Extending the hierarchy beyond the first level
==================

Using class ``Node``, one can build as many levels of hierarchy as
needed. In the following example, we build one additional hierarchy
level. 

The following script encapsuletes all the tasks considered above,
in addition to one new task: todays date:

<input directory="examples" read="m.py" content="python" action="show" flags="show_filename"/>

Indeed, we execute from the shell, a few of the above considered examples:

<input directory="examples" content="shell" action="execute">
python m.py today
python m.py n a 5 -n 10
python m.py n f
</input>

Similarly, from the Python prompt:

<input directory="examples" content="python" action="execute">
import m

m.T().sdigest('today')
m.T().sdigest('n a 5 -n 10')
for x in m.T().sdigest('n f',display=True):
    print('Also, printing here:', x )
</input>




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

