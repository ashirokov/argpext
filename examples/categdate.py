

import argpext

from argpext import *
import time

def today():
    "Return todays date in YYYY-MM-DD representation"
    return time.strftime('%Y-%m-%d', time.localtime())

dates = KeyWords([
    '1977-02-04',
    'Lisas birthday',
    'y2kday',
    'today'
])



str(dates)

dates('1977-02-04')
dates('Lisas birthday') 
dates('y2kday') 
dates('today') # Function today() is implicitly invoked at this line.
dates('2012-01-11') # Value not predefined
