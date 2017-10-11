import os
import re
import datetime
from datetime import timedelta


filePath = "/home/wmlab/Desktop/Botnet_Dataset/Sality/dumpTXT/newfiles0.txt"

file = open(filePath, 'r')
for line in file:
    # print type(line[:28])
    # print line[:28]
    data = []
    data.append(datetime.datetime.strptime(line[:28], "%b %d, %Y %H:%M:%S.%f"))
    print data
    line = re.split("\t|,", line[36:-1])
    data += line
    print data