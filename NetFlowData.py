# 'D:\Botnet\record'
# 2017-02-28 23:54:50.750
import os
import re
import datetime
from datetime import timedelta

# Preprocessing a csv file, and drop data which is not complete
# Return a dict-list of data
def Csv2DictList(filePath):
    sourceFile = open(filePath, 'r')
    fieldName = ['Date flow start','Duration','Proto','Src IP Addr','Src Port',
                 'Dst IP Addr','Dst Port','Packets','Bytes','Flow']
    dataList = []

    sourceFile.readline()
    lineNum = 0
    for line in sourceFile:
        # End of Data
        if line.find('Summary') != -1:
            break

        # Get data from string
        line = line.replace(" M", "M")
        line = line.replace(" K", "K")
        line = line[:-1]
        data = re.split(r" +-> +| {1,}|:|,+",line[24:])

        # print len(data)

        if len(data) < 10:
            print "File: " + filePath + ", At line: " + str(lineNum) + ", the field num in row is: " + str(len(data))
            break

        data[0] = line[:23]
        for j in range(7,9):
            data[j] = data[j].replace("M", " M")
            data[j] = data[j].replace("K", " K")

        # Convert data to dictionary type
        i = 0
        row = {}
        for name in fieldName:
            # row[name] = data[i]
            if i == 0:
                row[name] = datetime.datetime.strptime(data[i], "%Y-%m-%d %H:%M:%S.%f")
            else:
                row[name] = data[i]
            i += 1

        # print row
        # Append to dataList
        dataList.append(row)
    
    # print dataList[6]
    return dataList

# pick port number is 443 or 8080 
# seperate from src and dst
def ReduceByPort(dataList):
    srcList = []
    dstList = []
    serverList = []
    for data in dataList:
        if (data.get('Src Port') == '443') | (data.get('Src Port') == '8080'):
            srcList.append(data)
        elif (data.get('Dst Port') == '443') | (data.get('Dst Port') == '8080'):
            dstList.append(data)
    srcList = sorted(srcList, key=lambda k: k['Src IP Addr'])
    dstList = sorted(dstList, key=lambda k: k['Dst IP Addr'])
    serverList.append(srcList)
    serverList.append(dstList)
    return serverList

# create dict for each IP in serverList
def SeparateByIP(serverList, type):
    serverDict = {}
    newDictList = []
    i = 0
    selectIP = serverList[0].get(type)
    while i < len(serverList):
        if serverList[i].get(type) == selectIP:
            newDictList.append(serverList[i])
            if i == (len(serverList)-1):
                serverDict.update({selectIP:newDictList})
        else:                                              # a different IP
            serverDict.update({selectIP:newDictList})
            newDictList = []
            selectIP = serverList[i].get(type)
            newDictList.append(serverList[i])
            if i == (len(serverList)-1):                # the last IP different with privious IP
                serverDict.update({selectIP:newDictList})  # put it into serverDict directly
                # print "the last IP different with privious IP"
        i += 1

    cnt = 0
    for k in serverDict.keys():
        cnt += len(serverDict.get(k))
    # print ("cnt: " + str(cnt))
    # print ("len: " + str(len(serverList)))
    return serverDict

def SplitByHour(serverDict, startStamp):
    # Return a new serverDict may be better
    newDict = {} # k: IP address, value: dict(timeDict) of dataList (tempList)
    for s in serverDict.keys(): # Every 's' in 'serverDict.keys()' is an IP address

        print "==== START OF " + s + " =======\n\n"
        count = 0               # Count the line processed
        tempList = []           # Data will be stored in 'tempList' hour by hour
        timeDict = {}           # Create a dict to store data with {timeInterval:tempList}
        timeInterval = 0        # Number of time time interval
        tempStamp = startStamp  # 'tempStamp' will walk hour by hour

        for row in serverDict.get(s):
            if row.get('Date flow start') < startStamp:
                pass
            elif (row.get('Date flow start') - tempStamp) < timedelta(hours = 1):
                tempList.append(row)
                if count == len(serverDict.get(s))-1:
                    timeDict.update({timeInterval:tempList})
            else:
                timeDict.update({timeInterval:tempList})
                tempList = []
                timeInterval += 1
                tempStamp += timedelta(hours = 1)
                tempList.append(row)
            count += 1

        newDict.update({s:timeDict})
        print "====== END OF " + s + " =======\n\n"
    return newDict


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
sortedList = []
for s in serverList:
    for l in s:
        sortedList.append(l)
sortedList = sorted(sortedList, key=lambda k: k['Date flow start'])
for s in serverList:
    for l in s:
        print (l)
"""
# for s in serverList:
#     for data in s:
#         print data


# d1 = datetime.datetime.strptime("2017-02-28 23:54:50.750", "%Y-%m-%d %H:%M:%S.%f")
# d2 = datetime.datetime.strptime("2017-03-01 00:54:50.750", "%Y-%m-%d %H:%M:%S.%f")
# if (d2 - d1) >= timedelta(hours = 1):
#     print d2 - d1