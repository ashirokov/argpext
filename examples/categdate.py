#!/usr/bin/env python3

from argpext import *
import time

def today():
    "Return todays date in YYYY-MM-DD representation"
    return time.strftime('%Y-%m-%d', time.localtime())

dates = Categorical([
        '1977-02-04',
        ['Lisas birthday', '1977-01-01' ],
        ['y2kday', Unit(value='2000-01-01',help="The year 2000 date.") ],
        ['today' , Unit(value=today,callable=True,help="Today's date") ] 
        ])

str(dates)

dates('1977-02-04')
dates('Lisas birthday') 
dates('y2kday') 
dates('today') # Function today() is implicitly invoked at this line.
dates('2012-01-11') # Value not predefined
