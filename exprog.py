
import os
import sys

from subprocess import *

args = sys.argv[1:]


def notraceback(q):
    L = []
    if len(q):
        q = q.splitlines()
        for q in q:
            if q.startswith('Traceback '): continue
            if q.startswith(' '): continue
            L += [q]
    return os.linesep.join(L)


print('$ '+' '.join( args ) )

proc = Popen( args, stderr=PIPE, stdout=PIPE )

proc.wait()

L = []

# Deal with stdout
q = proc.stdout.read().decode()

if len(q): 
    q = q.splitlines()
    for q in q:
        q = q.replace('usage: ./','usage: ')
        print(q)




# Deal with stderr
q = proc.stderr.read().decode()
q = notraceback(q)

# display all
for line in q.splitlines():
    print( line )



