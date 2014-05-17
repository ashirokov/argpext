

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
    , long_description="""Argpext is a package that provides a collection of tools centred at
research and infrastructure development.

It allows one to quickly expose any selected Python functions to command
line interface for DOS or Linux-like shells. The user is responsible for organizing 
the required Python functions into a hierarchical tree-like structure, according to their logic
with tools provided by the package. Any such function then corresponds to a specific sequence of 
command line arguments which, when executed 
from the command line followed by the "--help" flag produces a detailed
help message. In order to execute the function, the rest of the command 
line arguments are filled based on the help message. 

A detailed documentation is currently available only for version 1.1.
Version 1.2.X will be documented within the next few weeks.

Release v1.1 - multiple new features. Detailed documentation is provided.

Release v1.2.0 - multiple new features

Release v1.2.1 - bug fixes for v1.2.0
"""
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

