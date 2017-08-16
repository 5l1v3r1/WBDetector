# 'D:\Botnet\record'
# 2017-02-28 23:54:50.750
import os
import re
import datetime
from datetime import timedelta

# 預處理一個 csv 檔, 不完整的 row data 就丟掉
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
            print ("File: " + filePath + ", At line: " + lineNum + ", the field num in row is: " + len(data))
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

# 挑出 port number 為 443 或 8080 的
# 分成 Src 與 Dst, 依照 IP 排序
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

# 把 serverList 依照 IP 建立 dict
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
    print ("cnt: " + str(cnt))
    print ("len: " + str(len(serverList)))

# d1 = datetime.datetime.strptime("2017-02-28 23:54:50.750", "%Y-%m-%d %H:%M:%S.%f")
# d2 = datetime.datetime.strptime("2017-03-01 00:54:50.750", "%Y-%m-%d %H:%M:%S.%f")
# if (d2 - d1) >= timedelta(hours = 1):
#     print d2 - d1

# dataList = Csv2DictList('/mnt/hgfs/Botnet/201703032000.csv')
# dataList = Csv2DictList('/mnt/hgfs/Botnet/201703011530.csv')
dataList = Csv2DictList('/mnt/hgfs/Botnet/tempCSV.csv')
serverList = ReduceByPort(dataList)
print ("src")
SeparateByIP(serverList[0], 'Src IP Addr')
print ("dst")
SeparateByIP(serverList[1], 'Dst IP Addr')
sortedList = []
for s in serverList:
    for l in s:
        sortedList.append(l)
sortedList = sorted(sortedList, key=lambda k: k['Date flow start'])
for s in serverList:
    for l in s:
        print (l)

# for s in serverList:
#     for data in s:
#         print data