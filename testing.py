import os
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