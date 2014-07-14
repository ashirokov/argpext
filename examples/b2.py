

def f():
    print('executing..')
    return [i for i in range(4)]

import argpext

class F(argpext.Task):
    hook = argpext.custom_hook(display=True)(f)

if __name__ == '__main__':
    F().digest()
