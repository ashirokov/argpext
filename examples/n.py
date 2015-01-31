
from argpext import Node

import a, b, c, d, e, f

class T(Node):
    "Integer range sequence methods"
    SUBS = [
        ('a', a.T),
        ('b', b.T),
        ('c', c.T),
        ('d', d.T),
        ('e', e.T),
        ('f', f.T),
    ]

if __name__ == '__main__':
    T().tdigest()




