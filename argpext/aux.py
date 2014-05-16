import argpext
from argpext import *

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


