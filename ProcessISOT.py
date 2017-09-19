

import os
import re
import ast
import datetime
from datetime import timedelta

# Take all the data in ISOT
# And use malicious IP to calculate threshold
def Text2DataList(filePath):
    fieldName = ['Date flow start', 'Proto', 'Src IP Addr', 'Dst IP Addr', 'Src Port', 'Dst Port', 'Bytes']

    count = 0
    dataList = []
    file = open(filePath, 'r')
    for line in file:
        count += 1
        tempDict = {}
        data = []
        data.append(datetime.datetime.strptime(line[:28], "%b %d, %Y %H:%M:%S.%f"))

        line = re.split("\t|,", line[36:-1])
        line = filter(None, line)

        if len(line) < 6:
            print "Column too few: " + filePath + ", at line: " + str(count)

        else:
            data += line
            i = 0
            for name in fieldName:
                tempDict[name] = data[i]
                i += 1
            dataList.append(tempDict)

    return dataList

def ReduceByPort(dataList):
    serverList = dataList

    # Skip selecting port
    """
    serverList = []
    for data in dataList:
        if (data.get('Src Port') == '443') | (data.get('Src Port') == '80'):
                serverList.append(data)
    """

    # Sort by IP address
    serverList = sorted(serverList, key=lambda k: k['Src IP Addr'])

    return serverList

def SeparateByIP(serverList):
    serverDict = {}
    newDictList = []
    i = 0
    # Take the first IP as 'selectIP'
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
            dataList = Text2DataList(filePath)
            serverList = ReduceByPort(dataList)

            if len(serverList) > 0:
                serverDict = SeparateByIP(serverList)

            for k in serverDict:
                outFile = open(tempPath + '\\' + k + ".txt", 'a')
                for row in serverDict[k]:
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

def PartII(tempPath, startStamp, endStamp, savePath, maliciousIP):
    count = 0
    for root, dirs, files in os.walk(tempPath):
        for name in files:
            if name in maliciousIP:
                path = os.path.join(root, name)
                ExtractFactor(path, startStamp, endStamp, savePath)
            count += 1
            print "Process Rate: " + str(count) + " / " + str(len(files))

if __name__ == '__main__':

    filePath = "D:\\Botnet\\isotCSV"
    tempPath = "D:\\Botnet\\TempISOT_withoutPort"
    savePath = 'D:\\Botnet\\WBDetector\\ISOT_IP_without.csv'

    maliciousIP = ['172.16.2.11', '172.16.0.2', '172.16.0.11', '172.16.0.12', \
                   '172.16.2.2', '172.16.2.3', '172.16.2.11', '172.16.2.12', \
                   '172.16.2.12', '172.16.2.12', '172.16.2.13', '172.16.2.14', \
                   '172.16.2.111', '172.16.2.112', '172.16.2.113', '172.16.2.114' ]

    # PartI(filePath, tempPath)
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