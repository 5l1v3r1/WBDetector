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
    sourceFile.close()
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

# Create dict for each IP in serverLis
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
    srcDict = {}
    dstDict = {}

    dataList = Csv2DictList(filePath)
    serverList = ReduceByPort(dataList)

    if filePath == 'D:\\Botnet\\record\\201703010005.csv':
        print serverList

    if len(serverList[0]) > 0:
        srcDict = SeparateByIP(serverList[0], 'Src IP Addr')
    if len(serverList[1]) > 0:
        dstDict = SeparateByIP(serverList[1], 'Dst IP Addr')


    # Check keys in the srcDict and dstDict or not
    # If the key is in srcDict or dstDict already, append its value into srcDict.get(k)
    # Or update a (k, v) with the new key and its value
    for k in srcDict:
        if mergeList[0].get(k) == None:
            mergeList[0].update({k:srcDict.get(k)})
        else:
            newList = mergeList[0].get(k)
            for item in srcDict.get(k):
                newList.append(item)
            mergeList[0].update({k: newList})

    for k in dstDict:
        if mergeList[1].get(k) == None:
            mergeList[1].update({k:dstDict.get(k)})
        else:
            newList = mergeList[1].get(k)
            for item in dstDict.get(k):
                newList.append(item)
            mergeList[1].update({k: newList})

    return mergeList

def Time2Interval(time, startStamp):
    t = (time - startStamp).days, (time - startStamp).seconds//3600
    return t[0] * 24 + t[1]

def SplitByHour(serverDict, startStamp):
    # Return a new serverDict may be better
    newDict = {} # k: IP address, value: dict(timeDict) of dataList (tempList)
    for s in serverDict.keys(): # Every 's' in 'serverDict.keys()' is an IP address

        # print "==== START OF " + s + " =======\n\n"
        tempList = []           # Data will be stored in 'tempList' hour by hour
        timeDict = {}           # Create a dict to store data with {timeInterval:tempList}

        for row in serverDict.get(s):
            if row.get('Date flow start') < startStamp:
                pass
            else:
                timeInterval = Time2Interval(row.get('Date flow start'), startStamp)
                if timeInterval in timeDict:
                    tempList = timeDict.get(timeInterval)
                else:
                    tempList = []

                tempList.append(row)
                timeDict.update({timeInterval:tempList})

        newDict.update({s:timeDict})

        # print "====== END OF " + s + " =======\n\n"
    return newDict
########################################## MAIN ##########################################


startStamp = datetime.datetime.strptime("2017-03-01 00:00:00.000", "%Y-%m-%d %H:%M:%S.%f")

mergeList = [{},{}]
#for root, dirs, files in os.walk('D:\\Botnet\\WBDetector\\testCSV'):
for root, dirs, files in os.walk('D:\\Botnet\\record'):
    for name in files:
        filePath = os.path.join(root, name)
        print filePath
        mergeList = ProcessFile(mergeList, filePath)
        print


srcDict = SplitByHour(mergeList[0], startStamp)
print ("src")
for s in srcDict:
    print type(srcDict.get(s))
    for k in srcDict.get(s):
        print k
        print type(srcDict.get(s).get(k))
        for row in srcDict.get(s).get(k):
            print row
        print "-------\n\n"

dstDict = SplitByHour(mergeList[1], startStamp)
print ("dst")
for s in dstDict:
    print type(dstDict.get(s))
    for k in dstDict.get(s):
        print k
        print type(dstDict.get(s).get(k))
        for row in dstDict.get(s).get(k):
            print row
        print "-------\n\n"
