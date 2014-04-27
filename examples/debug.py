#!/usr/bin/env python

import argpext

pri = argpext.DebugPrint(1,tr=1)


for i in range(1000):
    pri('here',s=99,e=102)


