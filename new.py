import os
import re
import datetime
from datetime import timedelta

def Time2Interval(time, startStamp):
    t = (time - startStamp).days, (time - startStamp).seconds//3600
    return t[0] * 24 + t[1]
"""
t0 = (datetime.datetime.strptime("2017-10-10 00:00:00.000", "%Y-%m-%d %H:%M:%S.%f"))
t1 = (datetime.datetime.strptime("2017-10-20 00:00:00.000", "%Y-%m-%d %H:%M:%S.%f"))

print t1 - t0

time = Time2Interval(t1, t0)

print time
"""

def ExtractFactors(startStamp, endStamp):
    t = Time2Interval(endStamp, startStamp)
    print t
    tempStart = startStamp
    while tempStart < endStamp:
        tempEnd = tempStart + timedelta(hours=2)
        if tempEnd > endStamp:
            break
        
        # do something here
        print tempStart, tempEnd
        tempStart = tempStart + timedelta(hours=1)

        # escapeIP = []
        # # for root, dirs, files in os.walk(tempPath + '\\srcServer'):
        # for root, dirs, files in os.walk(tempPath + '/srcServer'):
        #     for name in files:
        #         # print name
        #         # path = os.path.join(root, name)
        #         escapeIP += self.ExtractOne(tempPath, name, startStamp, endStamp, savePath)
    pass

t0 = (datetime.datetime.strptime("2017-10-10 00:00:00.000", "%Y-%m-%d %H:%M:%S.%f"))
t1 = (datetime.datetime.strptime("2017-10-15 00:00:00.000", "%Y-%m-%d %H:%M:%S.%f"))

ExtractFactors(t0, t1)