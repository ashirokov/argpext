import argpext
from argpext import *

#> Position 
class FrameRef:
    KEYS = keywords.KeyWords(['line','path','name','basename','smart_basename'])

    def __init__(self,up=0):
        self.frame = sys._getframe(1+up)

    def keys(self):
        return self.KEYS

    def __getitem__(self,key):
        "returns frame reference string"
        if self.KEYS(key) == 'line':
            return self.frame.f_lineno
        elif key == 'path':
            return self.frame.f_code.co_filename
        elif key == 'name':
            return self.frame.f_code.co_name
        elif key == 'basename':
            return os.path.basename(self['path'])
        elif key == 'smart_basename':
            basename = self['basename']
            q = self['path']
            q = os.path.dirname(q)
            q = os.path.basename(q)
            dirbasename = q
            return os.path.join( * (([dirbasename] if basename.lower() == '__init__.py' else [])+[basename]) )
        else:
            raise KeyError()


def chainref(fstr='%(name)s[%(smart_basename)s:%(line)s]',sep=' < ',up=0,limit=None):
    "Return chain reference."
    i = 0
    L = []
    while 1:
        try:
            f = fstr % FrameRef(up=1+up+i)
        except ValueError:
            break
        L += [f]
        i += 1
        if limit is not None and i == limit: break
    return sep.join(L)


class DebugPrint(object):

    def __init__(self,active=True,format_spec='{smart_basename}:{line} [{count}]: {string}'):

        # First thing off, check the highest priority argument.
        if not isinstance(active,(bool,int)): raise TypeError()
        self.active = active
        if not active: return

        self.format_spec = format_spec


    KEYS = keywords.KeyWords(['sep','end','file','flush',
                                      's','e','n'])

    def __call__(self,*args,**kwds):

        # First thing off, check the highest priority argument.
        if not self.active: return

        def active():
            # Update the count
            F = sys._getframe(2)
            line = F.f_lineno
            key = '__argpext_DebugPrint_%s' % line
            count = F.f_globals.setdefault(key,-1)
            count += 1
            F.f_globals[key] = count

            live = True
            # Process the restrictions
            s = kwds.pop('s')
            e = kwds.pop('e')
            if s is not None and count < s: live = False
            if e is not None and count >= e: live = False

            # Process the permissions
            n = kwds.pop('n')
            if n is not None and count == n: live = True

            return count,live

        count,live = active()
        if not live: return


        # print arguments
        sep = kwds.pop('sep',' ')
        end = kwds.pop('end','\n')
        file = kwds.pop('file',sys.stdout)
        flush = kwds.pop('flush',False)

        if len(kwds): raise KeyError('unrecognized keys: %s' % ( ','.join(kwds.keys()) ) )

        frm = {}
        frm.update( FrameRef(up=1) )
        frm['count'] = count


        string = sep.join([str(q) for q in args])+end

        q = frm
        q.update(dict(string=string))
        line = self.format_spec.format(**q)

        file.write(line)
        if flush: file.flush()

