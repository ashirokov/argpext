

def f():
    print('executing..')
    return [i for i in range(4)]

from argpext import *

class F(Task):
    hook = custom_hook()(f)

if __name__ == '__main__':
    F().digest()
