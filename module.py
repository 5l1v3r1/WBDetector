

import os
import re
import ast
import csv
import datetime
from datetime import timedelta

class PcapToData():
    pass    

class DataToFactors():

    # Declare variables and check paths are fine.
    def __init__(self, filePath, tempPath, savePath, startStamp, endStamp, isBotnet):
        self.filePath = filePath
        self.tempPath = tempPath
        self.savePath = savePath
        self.startStamp = startStamp
        self.endStamp = endStamp
        self.isBotnet = isBotnet

        if not os.path.exists(self.tempPath):
            os.mkdir(self.tempPath)

        if os.path.exists(self.savePath):
            os.remove(self.savePath)

        result = ["IP", "THR", "AC", "PSS"]
        with open(savePath, 'ab') as f:
            writer = csv.writer(f)
            writer.writerow(result)

        pass

    ######################### Arrange Data #########################

    # Preprocess a csv file, and drop data which is not complete
    # Return a dict-list of data
    def Csv2DictList(self, filePath):
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


            # The row of data is not complete, since there are 10 field in a row
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

    # Take all the data in Malicious Dataset
    def Text2DataList(self, filePath):
        fieldName = ['Date flow start', 'Proto', 'Src IP Addr', 'Dst IP Addr', 'Src Port', 'Dst Port', 'Bytes']

        count = 0
        dataList = []
        file = open(filePath, 'r')
        for line in file:
            count += 1
            tempDict = {}
            data = []
            # data[0] = line[:28]

            line = re.split("\t|,", line[36:-1])
            line = filter(None, line)

            if len(line) < 6:
                print "Column too few: " + filePath + ", at line: " + str(count)

            else:
                # data += line
                # data.append(line[:28])
                line.insert(0, line[:28])
                i = 0
                for name in fieldName:
                    if i == 0:
                        row[name] = datetime.datetime.strptime(line[i], "%Y-%m-%d %H:%M:%S.%f")
                    else:
                        tempDict[name] = line[i]
                    i += 1
                dataList.append(tempDict)

        return dataList

    # Pick port number == 443 or 8080 
    # Seperate from src and dst
    # Return a summary list of 2 list
    def ReduceByPort(self, dataList):
        srcList = []
        dstList = []
        serverList = []
        for data in dataList:
            if (data.get('Src Port') == '443') | (data.get('Src Port') == '8080') | (data.get('Src Port') == '80'):
                srcList.append(data)
            if (data.get('Dst Port') == '443') | (data.get('Dst Port') == '8080') | (data.get('Src Port') == '8080'):
                dstList.append(data)
        srcList = sorted(srcList, key=lambda k: k['Src IP Addr']) # Sort by IP address
        dstList = sorted(dstList, key=lambda k: k['Dst IP Addr']) # Sort by IP address
        serverList.append(srcList)
        serverList.append(dstList)
        return serverList

    # Create dict for each IP in serverLis
    def SeparateByIP(self, serverList, type):
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
        """
        cnt = 0
        for k in serverDict.keys():
            cnt += len(serverDict.get(k))
        print ("cnt: " + str(cnt))
        print ("len: " + str(len(serverList)))
        """
        return serverDict

    # Use the functions above to arrange data
    def ArrangeData(self, filePath, tempPath, isBotnet):
        # if not os.path.exists(tempPath + '\\srcServer'):
        #     os.mkdir(tempPath + '\\srcServer')
        # if not os.path.exists(tempPath + '\\dstServer'):
        #     os.mkdir(tempPath + '\\dstServer')

        if not os.path.exists(tempPath + '/srcServer/'):
            os.mkdir(tempPath + '/srcServer/')
        if not os.path.exists(tempPath + '/dstServer/'):
            os.mkdir(tempPath + '/dstServer/')

        for root, dirs, files in os.walk(filePath):

            count = 0
            for name in files:
                count += 1
                filePath = os.path.join(root, name)

                dataList = []
                if isBotnet:
                    dataList = self.Text2DataList(filePath)
                else:
                    dataList = self.Csv2DictList(filePath)
                serverList = self.ReduceByPort(dataList)

                srcDict = {}
                dstDict = {}

                if len(serverList[0]) > 0:
                    srcDict = self.SeparateByIP(serverList[0], 'Src IP Addr')
                if len(serverList[1]) > 0:
                    dstDict = self.SeparateByIP(serverList[1], 'Dst IP Addr')

                for k in srcDict:
                    # outFile = open(tempPath + '\\srcServer\\' + k + ".txt", 'a')
                    outFile = open(tempPath + '/srcServer/' + k + ".txt", 'a')
                    for row in srcDict[k]:
                        outFile.write(str(row) + "\n")

                for k in dstDict:
                    # outFile = open(tempPath + '\\dstServer\\' + k + ".txt", 'a')
                    outFile = open(tempPath + '/dstServer/' + k + ".txt", 'a')
                    for row in dstDict[k]:
                        outFile.write(str(row) + "\n")

                print "Process Rate: " + str(count) + " / " + str(len(files))

    ####################### Extract Factors ########################

    def ReadServerFile(self, path):
        dataList = []
        try:
            file = open(path, 'r')
            for line in file:
                dataList.append(eval(line))
        except Exception as e:
            print e


        return dataList

    def Time2Interval(self, time, startStamp):
        t = (time - startStamp).days, (time - startStamp).seconds//3600
        return t[0] * 24 + t[1]

    def SplitByHour(self, dataList, startStamp, endStamp):
        tempList = []           # Data will be stored in 'tempList' hour by hour
        timeDict = {}           # Create a dict to store data with {timeInterval:tempList}

        for row in dataList:
            if row.get('Date flow start') < startStamp:
                pass
            elif row.get('Date flow start') >= endStamp:
                pass
            else:
                timeInterval = self.Time2Interval(row.get('Date flow start'), startStamp)
                if timeInterval in timeDict:
                    tempList = timeDict.get(timeInterval)
                else:
                    tempList = []

                tempList.append(row)
                timeDict.update({timeInterval:tempList})
        return timeDict

    def GetMaxSize(self, timeDict):
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

    def GetHostGroup(self, timeDict, selectType):
        hostGroup = {}
        for t in timeDict:
            hosts = []
            for row in timeDict[t]:
                hosts.append(row.get(selectType))
            hosts = set(hosts)
            hostGroup.update({t:hosts})
        return hostGroup

    def MergeHostGroup(self, hostGroupSrc, hostGroupDst):
        hostGroup = {}
        hostGroup = hostGroupSrc

        for t in hostGroupDst:
            if t in hostGroup:
                newHosts = hostGroup.get(t) | hostGroupDst.get(t)
                hostGroup.update({t:newHosts})
            else:
                hostGroup.update({t:hostGroupDst.get(t)})
        return hostGroup

    def ExtractOne(self, tempPath, name, startStamp, endStamp, savePath):
        dataList = []
        timeDict = {}

        maxSize = {}   # k: timeInterval, v: byte
        hostGroupSrc = {} # k: timeInterval, v: set(hostIP)

        escapeIP = []

        path = tempPath + '\\srcServer\\' + name
        dataList = self.ReadServerFile(path)
        timeDict = self.SplitByHour(dataList, startStamp, endStamp)
        maxSize = self.GetMaxSize(timeDict)
        hostGroupSrc = self.GetHostGroup(timeDict, 'Dst IP Addr')

        # If the srcIP in dstServer, the hostgroup should be union
        path = tempPath + '\\dstServer\\' + name
        if os.path.exists(path):
            escapeIP.append(name)
            dataList = self.ReadServerFile(path)
            self.SplitByHour(dataList, startStamp, endStamp)
            hostGroupDst = self.GetHostGroup(timeDict, 'Src IP Addr')
            hostGroup = self.MergeHostGroup(hostGroupSrc, hostGroupDst)
        else:
            hostGroup = hostGroupSrc

        i = 1
        n = 72
        thr_sigma = 0
        acs_sigma = 0
        pss_sigma = 0

        while i < 72:
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

        result = [name[:-4], str(THR), str(AC), str(PSS)]
        with open(savePath, 'ab') as f:
            writer = csv.writer(f)
            writer.writerow(result)

        return escapeIP

    def ExtractFactors(self, tempPath, startStamp, endStamp, savePath):
        t = 0 # 72 hours: t0 ~ t71
        escapeIP = []
        for root, dirs, files in os.walk(tempPath + '\\srcServer'):
            for name in files:
                # print name
                # path = os.path.join(root, name)
                escapeIP += self.ExtractOne(tempPath, name, startStamp, endStamp, savePath)
        pass

if __name__ == '__main__':
    
    """ NCU data
    filePath = "D:\\Botnet\\record"
    tempPath = "D:\\Botnet\\TempFile-revise"
    savePath = "D:\\Botnet\\revise\\recordFactor_02_05.csv"
    startStamp = datetime.datetime.strptime("2017-03-02 00:00:00.000", "%Y-%m-%d %H:%M:%S.%f")
    endStamp = datetime.datetime.strptime("2017-03-05 00:00:00.000", "%Y-%m-%d %H:%M:%S.%f")
    isBotnet = False
    """

    # """ BOTNET data
    filePath = "/home/wmlab/Desktop/Botnet_Dataset/Sality/splited"
    tempPath = "/home/wmlab/Desktop/Botnet_Dataset/Sality/tempFile"
    savePath = "/home/wmlab/Desktop/Botnet_Dataset/Sality/Factors.csv"
    startStamp = datetime.datetime.strptime("2014-02-20 00:00:00.000", "%Y-%m-%d %H:%M:%S.%f")
    endStamp = datetime.datetime.strptime("2014-04-07 00:00:00.000", "%Y-%m-%d %H:%M:%S.%f")
    isBotnet = True
    # """

    
    # Create a instance
    worker = DataToFactors(filePath, tempPath, savePath, startStamp, endStamp, isBotnet)

    worker.ArrangeData(worker.filePath, worker.tempPath, worker.isBotnet)
    print "TempFiles OK"
    
    # worker.ExtractFactors(worker.tempPath, worker.startStamp, worker.endStamp, worker.savePath)
    # print "FactorsFils OK"
