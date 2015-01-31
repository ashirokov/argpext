
import datetime

from argpext import Task, Node, customize

import n, a

class Today(Task):
    @customize(tostring=str)
    def hook(self):
        "Return todays date"
        return datetime.datetime.today().date()

class T(Node):
    "All tasks in one script"
    SUBS = [
        ('today', Today),
        ('n', n.T),
        ]

if __name__ == '__main__':
    T().tdigest()




