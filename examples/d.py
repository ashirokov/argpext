from argpext import *

class T(Task):
    def hook(self):
        "Return integers 1 to 3"
        return [1,2,3]

if __name__ == '__main__':
    T().tdigest()
