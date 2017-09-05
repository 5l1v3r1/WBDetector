

import os
import re
import ast
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
        line = line.replace(" G", "G")
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
            data[j] = data[j].replace("G", " G")

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
        if (data.get('Dst Port') == '443') | (data.get('Dst Port') == '8080'):
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

def PartI(filePath, tempPath):
    if not os.path.exists(tempPath + '\\srcServer'):
        os.mkdir(tempPath + '\\srcServer')
    if not os.path.exists(tempPath + '\\dstServer'):
        os.mkdir(tempPath + '\\dstServer')

    for root, dirs, files in os.walk(filePath):

        count = 0
        for name in files:
            count += 1
            filePath = os.path.join(root, name)

            dataList = []
            dataList = Csv2DictList(filePath)
            serverList = ReduceByPort(dataList)

            if len(serverList[0]) > 0:
                srcDict = SeparateByIP(serverList[0], 'Src IP Addr')
            if len(serverList[1]) > 0:
                dstDict = SeparateByIP(serverList[1], 'Dst IP Addr')

            for k in srcDict:
                outFile = open(tempPath + '\\srcServer\\' + k + ".txt", 'a')
                for row in srcDict[k]:
                    outFile.write(str(row) + "\n")

            for k in dstDict:
                outFile = open(tempPath + '\\dstServer\\' + k + ".txt", 'a')
                for row in dstDict[k]:
                    outFile.write(str(row) + "\n")

            print "Process Rate: " + str(count) + " / " + str(len(files))

filePath = 'D:\\Botnet\\record'
tempPath = 'D:\\Botnet\\TempAgain'
PartI(filePath, tempPath)