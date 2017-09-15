"""
import os
import subprocess

# get the work directory of this file
path = os.getcwd()+'/03/'

# recurrent search all directory/file under the path 
for tops, dirs, files in os.walk(path):
    for name in files:
        LogFilePath = os.path.join(tops, name)
        LogFilePath = "."+LogFilePath[len(os.getcwd()):]
        CsvFileName = name.split('.')[-1]+".csv"
        cmd = "nfdump -r "+LogFilePath+" | tee ./record/"+CsvFileName
        os.system(cmd)
"""

import os
import subprocess

# get the work directory of this file
# path = os.getcwd()+'\\03\\'
path = os.getcwd()+'\\dump\\'
# print path # D:\Botnet\03\

# recurrent search all directory/file under the path 
for tops, dirs, files in os.walk(path):
    for name in files:
        LogFilePath = os.path.join(tops, name)
        # print LogFilePath # D:\Botnet\03\08\nfcapd.201703080305
        LogFilePath = "."+LogFilePath[len(os.getcwd()):]
        # print LogFilePath # .\03\08\nfcapd.201703080305
        CsvFileName = name.split('.')[-1]+".csv"
        # print name.split('.') # ['nfcapd', '201703080305']
        # print CsvFileName # 201703080305.csv
        cmd = "nfdump -r " + LogFilePath + " | tee ./"+ CsvFileName
        # os.system(cmd)