from argpext import *


def represent_as_string(x):
    return "[element: %s]" % x

class C(Task):

    @customize(tostring=represent_as_string)
    def hook(self):
        "Return integers 1 to 3"
        for element in [1,2,3]:
            yield element

if __name__ == '__main__':
    C().tdigest()
