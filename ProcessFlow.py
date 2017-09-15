

import os
import re
import ast
import csv
import datetime
from datetime import timedelta

# Preprocessing a csv file, and drop data which is not complete
# Return a dict-list of data
def Csv2DataList(filePath):
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
            # print "File: " + filePath + \
            #       ", At line: " + str(lineNum) + \
            #       ", the field num in row is: " + str(len(data))
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

    srcList = sorted(srcList, key=lambda k: k['Src IP Addr']) # Sort by IP address
    return srcList

# Create dict for each IP in serverLis
def SeparateByIP(serverList):
    serverDict = {}
    newDictList = []
    i = 0
    selectIP = serverList[0].get('Src IP Addr')
    while i < len(serverList):
        if serverList[i].get('Src IP Addr') == selectIP:
            newDictList.append(serverList[i])
            # The last IP is the same with privious IP
            if i == (len(serverList)-1):
                serverDict.update({selectIP:newDictList})
        else: # A different IP
            serverDict.update({selectIP:newDictList})
            newDictList = []
            selectIP = serverList[i].get('Src IP Addr')
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

def PartI(filePath, tempPath):
    if not os.path.exists(tempPath):
        os.mkdir(tempPath)

    for root, dirs, files in os.walk(filePath):

        count = 0
        for name in files:
            count += 1
            filePath = os.path.join(root, name)

            dataList = []
            dataList = Csv2DataList(filePath)
            serverList = ReduceByPort(dataList)

            if len(serverList) > 0:
                srcDict = SeparateByIP(serverList)

            for k in srcDict:
                outFile = open(tempPath + '\\' + k + ".txt", 'a')
                for row in srcDict[k]:
                    outFile.write(str(row) + "\n")

            print "Process Rate: " + str(count) + " / " + str(len(files))

def ReadServerFile(path):
    dataList = []
    try:
        file = open(path, 'r')
        for line in file:
            dataList.append(eval(line))
    except Exception as e:
        print e


    return dataList

def Time2Interval(time, startStamp):
    t = (time - startStamp).days, (time - startStamp).seconds // 3600
    return t[0] * 24 + t[1] # t[0] days, t[1] hours

def SplitByHour(dataList, startStamp, endStamp):
    tempList = []           # Data will be stored in 'tempList' hour by hour
    timeDict = {}           # Create a dict to store data with {timeInterval:tempList}

    for row in dataList:
        if row.get('Date flow start') < startStamp:
            pass
        elif row.get('Date flow start') >= endStamp:
            pass
        else:
            timeInterval = Time2Interval(row.get('Date flow start'), startStamp)
            if timeInterval in timeDict:
                tempList = timeDict.get(timeInterval)
            else:
                tempList = []

            tempList.append(row)
            timeDict.update({timeInterval:tempList})
    return timeDict

def GetMaxSize(timeDict):
    maxSize = {}
    for t in timeDict:
        maxByte = 0.0
        for row in timeDict[t]:
            size = row.get('Bytes')
            if size.endswith('K'):
                size = float(size.replace('K', '')) * 1024
                row.update({'Bytes':size})
            elif size.endswith('M'):
                size = float(size.replace('M', '')) * 1024 * 1024
                row.update({'Bytes':size})

            if float(row.get('Bytes')) > maxByte:
                maxByte = float(row.get('Bytes'))
        maxSize.update({t:maxByte})
    return maxSize

def GetHostGroup(timeDict):
    hostGroup = {}
    for t in timeDict:
        hosts = []
        for row in timeDict[t]:
            hosts.append(row.get('Dst IP Addr'))
        hosts = set(hosts)
        hostGroup.update({t:hosts})
    return hostGroup

def ExtractFactor(path, startStamp, endStamp, savePath):
    dataList = []
    timeDict = {}

    maxSize = {}   # k: timeInterval, v: byte
    hostGroup = {} # k: timeInterval, v: set(hostIP)

    dataList = ReadServerFile(path)
    timeDict = SplitByHour(dataList, startStamp, endStamp)
    maxSize = GetMaxSize(timeDict)
    hostGroup = GetHostGroup(timeDict)

    i = 1
    n = 48
    thr_sigma = 0
    acs_sigma = 0
    pss_sigma = 0

    while i < 48:
        if hostGroup.get(i-1) == None:
            hostGroup.update({i-1:[]})
        if hostGroup.get(i) == None:
            hostGroup.update({i:[]})
        if maxSize.get(i) == None:
            maxSize.update({i:0})

        if len(set(hostGroup.get(i))) > 0:
            thr_sigma += float(len(set(hostGroup.get(i-1)) & set(hostGroup.get(i)))) / len(set(hostGroup.get(i)))
        acs_sigma += len(set(hostGroup.get(i)))
        pss_sigma += maxSize.get(i)

        i += 1

    THR = thr_sigma / n
    AC = acs_sigma
    if (AC == 0) & (pss_sigma == 0):
        PSS = 0
    else:
        PSS = pss_sigma / AC

    result = [path[19:-4], str(THR), str(AC), str(PSS)]
    with open(savePath, 'ab') as f:
        writer = csv.writer(f)
        writer.writerow(result)

def PartII(tempPath, startStamp, endStamp, savePath):
    count = 0
    for root, dirs, files in os.walk(tempPath):
        for name in files:
            path = os.path.join(root, name)
            ExtractFactor(path, startStamp, endStamp, savePath)
            count += 1
            print "Process Rate: " + str(count) + " / " + str(len(files))

if __name__ == '__main__':
    filePath = 'D:\\Botnet\\record'
    tempPath = 'D:\\Botnet\\TempFile'
    savePath = 'D:\\Botnet\\WBDetector\\FactorRecord_Mar06_07.csv'

    if os.path.exists(savePath):
        os.remove(savePath)

    result = ["IP", "THR", "AC", "PSS"]
    with open(savePath, 'ab') as f:
        writer = csv.writer(f)
        writer.writerow(result)

    startStamp = datetime.datetime.strptime("2017-03-06 00:00:00.000", "%Y-%m-%d %H:%M:%S.%f")
    endStamp = datetime.datetime.strptime("2017-03-07 00:00:00.000", "%Y-%m-%d %H:%M:%S.%f")
    # PartI(filePath, tempPath)
    PartII(tempPath, startStamp, endStamp, savePath)
