from argpext import *


def represent_as_string(x):
    return ','.join([str(q) for q in x])

class T(Task):

    @customize(tostring=represent_as_string)
    def hook(self):
        "Return integers 1 to 3"
        return [1,2,3]

if __name__ == '__main__':
    T().tdigest()
