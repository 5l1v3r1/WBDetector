

import os
import re
import ast
import datetime
from datetime import timedelta

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
    serverList = []

    for data in dataList:
        if (data.get('Src Port') == '443') | (data.get('Src Port') == '80'):
            serverList.append(data)

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


if __name__ == '__main__':

    # filePath = "D:\\Botnet\\isotCSV"
    tempPath = "D:\\Botnet\\tempISOT"


    filePath = "D:\\Botnet\\WBDetector\\TestTXT\\newfiles1100.txt"
    dataList = Text2DataList(filePath)
    serverList = ReduceByPort(dataList)
    if len(serverList) > 0:
        serverDict = SeparateByIP(serverList)

        for k in serverDict:
            outFile = open(tempPath + "\\" + k + ".txt", 'a')
            for row in serverDict[k]:
                outFile.write(str(row) + "\n")
