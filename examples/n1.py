
from argpext import *

import e3, e1, e4, a1, a3, a4

class Main(Node):
    SUBS = [
        ('e3', e3.F),
        ('e1', e1.G),
        ('e4', e4.F),
        ('a1', a1.C),
        ('a3', a3.C),
        ('a4', a4.C),
        ]

if __name__ == '__main__':
    Main().tdigest()




