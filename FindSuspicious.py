


import os
import csv

# Use the maximum of each factor to do judgement
thershold_THR = 0.59879
thershold_AC = 739
thershold_PSS = 155.5227

# Count the times of IP be judged as a malicious IP
countDict = {}

# Walk through all the csv file
folder = "D:\\Botnet\\WBDetector\\FactorRecord"

for root, dirs, files in os.walk(folder):
    for name in files:
        path = os.path.join(root, name)
        with open(path) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:

                IP = row['IP']
                THR = float(row['THR'])
                AC = float(row['AC'])
                PSS = float(row['PSS'])

                if IP == 'AVG':
                    break

                suspicious_HR = 0
                suspicious_PSS = 0
                suspicious_CC = 0
                

                if (THR > thershold_THR) & (AC < thershold_AC):
                    suspicious_HR = 1

                if PSS > thershold_PSS:
                    suspicious_PSS = 1

                if suspicious_PSS | suspicious_HR:
                    suspicious_CC = 1

                tempDict = {}

                if IP in countDict:
                    tempDict = countDict[IP]
                    tempDict['HR'] += suspicious_HR
                    tempDict['PSS'] += suspicious_PSS
                    tempDict['CC'] += suspicious_CC
                    countDict.update({IP:tempDict})
                else:
                    tempDict['HR'] = suspicious_HR
                    tempDict['PSS'] = suspicious_PSS
                    tempDict['CC'] = suspicious_CC
                    countDict.update({IP:tempDict})

for k in countDict:
    print k
    print countDict[k]
    print "=============================="
    print







