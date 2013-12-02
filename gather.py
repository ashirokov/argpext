#!/usr/bin/env python3


fhi = open('help.sh')
fho = open('gathers.py','w')

pyfiles = set()

for line in fhi:
    line = line.strip()
    if not line.startswith('$PY -m'): continue
    L = line.split()[2:]
    key = L.pop(0)
    pyfile = L.pop(0)

    i = L.index('>')
    commands = L[0:i]
    tmpfile = L[i+1]

    print( "%s('%s', args=%s, tmpfile='%s')" % (key, pyfile, commands,tmpfile) )
    #if pyfile not in pyfiles and pyfile != 'argpext.py':
    #    pystr = open(pyfile).read()
    #    pyvar = pyfile.split('.')[0]
    #    print("'%s' : '''" % pyvar)
    #    print( pystr )
    #    print("''',")
    #    print()
    #    pyfiles.add( pyfile )

fhi.close()
fho.close()

