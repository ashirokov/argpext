from argpext import *

class C(Task):
    def hook(self):
        "Return integers 1 to 3"
        return [1,2,3]

if __name__ == '__main__':
    C().tdigest()
