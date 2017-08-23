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
    sourceFile.readline() # Read the field name line
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

        # The row of data is not complete
        if len(data) < 10:
            print "File: " + filePath + \
                  ", At line: " + str(lineNum) + \
                  ", the field num in row is: " + str(len(data))
            break

        data[0] = line[:23]
        for j in range(7,9):
            data[j] = data[j].replace("M", " M")
            data[j] = data[j].replace("K", " K")

        # Put every column into dict with (k:v) = (fieldName:data)
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

    return dataList

# Pick port number == 443 or 8080 
# Seperate from src and dst
# Return a summary list of 2 list
def ReduceByPort(dataList):
    srcList = []
    dstList = []
    serverList = []
    for data in dataList:
        if (data.get('Src Port') == '443') | (data.get('Src Port') == '8080'):
            srcList.append(data)
        elif (data.get('Dst Port') == '443') | (data.get('Dst Port') == '8080'):
            dstList.append(data)
    srcList = sorted(srcList, key=lambda k: k['Src IP Addr']) # Sort by IP address
    dstList = sorted(dstList, key=lambda k: k['Dst IP Addr']) # Sort by IP address
    serverList.append(srcList)
    serverList.append(dstList)
    return serverList

# Create dict for each IP in serverList
def SeparateByIP(serverList, type):
    serverDict = {}
    newDictList = []
    i = 0
    selectIP = serverList[0].get(type)
    while i < len(serverList):
        if serverList[i].get(type) == selectIP:
            newDictList.append(serverList[i])
            # The last IP is the same with privious IP
            # 
            if i == (len(serverList)-1):
                serverDict.update({selectIP:newDictList})
        else: # A different IP
            serverDict.update({selectIP:newDictList})
            newDictList = []
            selectIP = serverList[i].get(type)
            newDictList.append(serverList[i])
            # The last IP different with privious IP
            # Put it into 'serverDict' directly
            if i == (len(serverList)-1): 
                serverDict.update({selectIP:newDictList})
        i += 1

    # cnt = 0
    # for k in serverDict.keys():
    #     cnt += len(serverDict.get(k))
    # print ("cnt: " + str(cnt))
    # print ("len: " + str(len(serverList)))
    return serverDict

# Call functions above to process a file
# Merge data into srcDict, dstDict
def ProcessFile(mergeList, filePath):
    dataList = []
    serverList = []
    srcTempDict = {}
    dstTempDict = {}

    dataList = Csv2DictList(filePath)
    serverList = ReduceByPort(dataList)
    srcDict = SeparateByIP(serverList[0], 'Src IP Addr')
    dstDict = SeparateByIP(serverList[1], 'Dst IP Addr')

    # Check keys in the srcTempDict and dstTempDict
    # If the key is in srcDict, dstDict already, append its value into srcDict.get(k)
    # Or update a (k, v)b with the new key and its value
    for k in srcDict:
        if mergeList[0].get(k) == None:
            mergeList[0].update({k:srcDict.get(k)})
        else:
            newList = mergeList[0].get(k)
            newList.append(srcDict.get(k))
            mergeList[0].update({k: newList})

    for k in dstDict:
        if mergeList[1].get(k) == None:
            mergeList[1].update({k:dstDict.get(k)})
        else:
            newList = mergeList[1].get(k)
            newList.append(dstDict.get(k))
            mergeList[0].update({k: newList})

    return mergeList

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

mergeList = [{},{}]
for root, dirs, files in os.walk("D:\\Desktop\\WBDetector\\testCSV"):
    for file in files:
        filePath = os.path.join(root, file)
        mergeList = ProcessFile(mergeList, filePath)

print "mergeList: " + str(len(mergeList))
print mergeList[0].get('140.115.135.25')
print mergeList[1].get('31.13.87.1')
# startStamp = datetime.datetime.strptime("2017-03-01 00:00:00.000", "%Y-%m-%d %H:%M:%S.%f")
# srcDict = SplitByHour(srcDict, startStamp)
# dstDict = SplitByHour(dstDict, startStamp)



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
