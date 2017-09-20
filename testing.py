import os
import csv
import datetime
from datetime import timedelta

# savePath = 'D:\\Botnet\\WBDetector\\FactorRecord.csv'
# result = [1, 2, 3]

# with open(savePath, 'ab') as f:
#     writer = csv.writer(f)
#     writer.writerow(result)

# def F(serverDict, startStamp):
#     # Return a new serverDict may be better
#     newDict = {} # k: IP address, value: dict(timeDict) of dataList (tempList)
#     for s in serverDict.keys(): # Every 's' in 'serverDict.keys()' is an IP address

#         print "==== START OF " + s + " =======\n\n"
#         count = 0               # Count the line processed
#         tempList = []           # Data will be stored in 'tempList' hour by hour
#         timeDict = {}           # Create a dict to store data with {timeInterval:tempList}

#         for row in serverDict.get(s):
#             if row.get('Date flow start') < startStamp:
#                 pass
#             else:
#                 timeInterval = str(row.get('Date flow start') - startStamp)
#                 if timeInterval in timeDict:
#                     tempList = timeDict.get(timeInterval)
#                 else:
#                     tempList = []

#                 tempList.append(row)
#                 timeDict.update({timeInterval:tempList})

#         newDict.update({s:timeDict})

#         print "====== END OF " + s + " =======\n\n"
#     return newDict


# def days_hours_minutes(td):
#     return td.days, td.seconds//3600 #, (td.seconds//60)%60

# def Time2Interval(time, t0):
#     t = (time - t0).days, (time - t0).seconds//3600
#     return t[0] * 24 + t[1]
#     return t


t0 = datetime.datetime.strptime("2007-10-08 00:00:00.000", "%Y-%m-%d %H:%M:%S.%f")
t1 = t0 + timedelta(hours = 47)

# print t0
print t1

# t1 = datetime.datetime.strptime("2017-03-01 00:59:00.000", "%Y-%m-%d %H:%M:%S.%f")
# t2 = datetime.datetime.strptime("2017-03-01 02:00:00.000", "%Y-%m-%d %H:%M:%S.%f")
# t3 = datetime.datetime.strptime("2017-03-01 03:05:00.080", "%Y-%m-%d %H:%M:%S.%f")
# t4 = datetime.datetime.strptime("2017-03-02 04:00:00.000", "%Y-%m-%d %H:%M:%S.%f")

# print  days_hours_minutes(t3-t0)
# print Time2Interval(t1, t0)

# l1 = set([1,3,5,7,9])
# l2 = set([0,2,4,6,8])
# print l1 + l2

""" Testing Area
dataList = Csv2DictList('spe.csv')
# for data in dataList:
#     print data

serverList = ReduceByPort(dataList)
# print ("src")
# for data in serverList[0]:
#     print data
# print ("dst")
# for data in serverList[1]:
#     print data



# print ("src")
srcDict = SeparateByIP(serverList[0], 'Src IP Addr')
# print (srcDict.keys()[0])
# for data in srcDict.get(srcDict.keys()[0]):
#     print data
# print ("------------------------------------------")

# print ("dst")
dstDict = SeparateByIP(serverList[1], 'Dst IP Addr')
# print (dstDict.keys()[0])
# for data in dstDict.get(dstDict.keys()[0]):
#     print data
# print ("------------------------------------------")


mergeList = [{},{}]
for root, dirs, files in os.walk("D:\\Botnet\\WBDetector\\testCSV"):
    for name in files:
        filePath = os.path.join(root, name)
        print filePath
        mergeList = ProcessFile(mergeList, filePath)
        print
        print
        print

for k in mergeList[0]:
    print "src: " + k
    for item in mergeList[0].get(k):
        print str(item) + "\n"
print
print

for k in mergeList[1]:
    print "dst: " + k
    for item in mergeList[1].get(k):
        print str(item) + "\n"
print
print

startStamp = datetime.datetime.strptime("2017-03-01 00:00:00.000", "%Y-%m-%d %H:%M:%S.%f")

srcDict = SplitByHour(srcDict, startStamp)
# print ("src")
# for s in srcDict:
#     print type(srcDict.get(s))
#     for k in srcDict.get(s):
#         print k
#         print type(srcDict.get(s).get(k))
#         for row in srcDict.get(s).get(k):
#             print row
#         print "-------\n\n"

dstDict = SplitByHour(dstDict, startStamp)
# print ("dst")
# for s in dstDict:
#     print type(dstDict.get(s))
#     for k in dstDict.get(s):
#         print k
#         print type(dstDict.get(s).get(k))
#         for row in dstDict.get(s).get(k):
#             print row
#         print "-------\n\n"
"""