

from distutils.core import setup

setup(
    name='argpext'
    , version='1.2.1'
    , description = 'Argpext: hierarchical extension of sub-commands in argparse.'
    , author='Alexander Shirokov'
    , author_email='alexander.shirokov@gmail.com'
    , packages=['argpext']
    , scripts = ['argpext.py']
    , py_modules=['argpext']
    , license='OSI Approved'
    , long_description="""Argpext is a Python package that provides a collection of tools centred on
research infrastructure development.

Argpext provides hierarchical (multilevel) subcommand implementation that
allows one to quickly expose any required callable objects, such as functions, 
generators, or any other Python's callable objects 
to the DOS/Linux command line. 

Hierarchical sub-commands implementation: 
Class "Task" is used to define the interface
between a specific callable object and the command line. Class "Node"
may be used in order to populate all the required "tasks" onto a tree structure,
whose design follows the intended execution patterns.
Any such task may then individually be executed by passing a specific
sequence of command line arguments to the top level script, followed
by the command line arguments used to specify the arguments, if required by the task. 
When followed by the "--help" flag,  such sequence simply outputs
the help message that provides short description of the task and directions
for populating task arguments. Passing the sequence of command 
complete with task arguments results in the actual execution of the task.
Hierarchical subcommands feature internally relies on the standard Pythons standard module.


A detailed documentation is currently available only for version 1.1; see link above.

Documentation for Version 1.2.X will be released approximately by the mid June 2014.

Release v1.1 - multiple new features. Detailed documentation is provided.

Release v1.2.0 - multiple new features

Release v1.2.1 - bug fixes for v1.2.0"""
    , classifiers = [
        'Development Status :: 4 - Beta'
        ,'Environment :: Console'
        ,'Intended Audience :: Developers'
        ,'Intended Audience :: Information Technology'
        ,'Intended Audience :: Science/Research'
        ,'Intended Audience :: End Users/Desktop'
        ,'Operating System :: MacOS :: MacOS X'
        ,'Operating System :: Microsoft :: Windows'
        ,'Operating System :: POSIX'
        ,'Programming Language :: Python :: 3'
        ,'Programming Language :: Python :: 2'

        ,'Topic :: Software Development :: User Interfaces'
        ,'Topic :: Software Development :: Interpreters'        
        ,'Topic :: Utilities'
    ]
)

