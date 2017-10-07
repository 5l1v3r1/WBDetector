

import os

oriPcap = "/home/wmlab/Desktop/Botnet_Dataset/Zeus/Zeus-2/2014-06-06_capture-win8.pcap"
fileDir = "/home/wmlab/Desktop/Botnet_Dataset/Zeus/Zeus-2/splited"
saveDir = "/home/wmlab/Desktop/Botnet_Dataset/Zeus/Zeus-2/dumpTXT"

if not os.path.exists(fileDir):
    os.mkdir(fileDir)
if not os.path.exists(saveDir):
    os.mkdir(saveDir)

# Split big origin file to several small file
splitCMD = "tcpdump -r " + oriPcap + " -w newfiles -U -C 10"
os.system(splitCMD)


# Move file to make process easier
moveCMD = "mv newfiles newfiles0 ; mv newfiles* " + fileDir
os.system(moveCMD)

print "Splitted!"

# Dump pcap to txt file
for root, dirs, files in os.walk(fileDir):
    print root
    count = 0
    for name in files:
        path = os.path.join(root, name)
        savePath = saveDir + "/" + name + ".txt"
        dumpCMD = "tshark -r " + path + " -T fields -e frame.time -e _ws.col.Protocol -e ip.src -e ip.dst -e tcp.port -e frame.len > " + savePath
        os.system(dumpCMD)
        count += 1
        print "Process Rate: " + str(count) + " / " + str(len(files))

print "Dumped!"