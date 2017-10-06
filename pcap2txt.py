import os

# oriPcap = "/home/wmlab/Desktop/Botnet_Dataset/Zeus/Zeus-1/2014-05-30_capture-win8.pcap"
fileDir = "/home/wmlab/Desktop/Botnet_Dataset/Zeus/Zeus-1/splited"

# if not os.path.exists(fileDir):
#     os.mkdir(fileDir)

# # Split big origin file to several small file
# splitCMD = "tcpdump -r " + oriPcap + " -w newfiles -U -C 10"
# os.system(splitCMD)


# Move file to make process easier
moveCMD = "mv newfiles newfiles0 ; mv newfiles* " + fileDir
os.system(moveCMD)

print "Splitted!"

# # Dump pcap to txt file
# if not os.path.exists(saveDir):
# 	os.mkdir(saveDir)

# for root, dirs, files in os.walk(fileDir):
#     print root
#     count = 0
#     for name in files:
#         path = os.path.join(root, name)
#         savePath = saveDir + "/" + name + ".txt"
#         dumpCMD = "tshark -r " + path + " -T fields -e frame.time -e _ws.col.Protocol -e ip.src -e ip.dst -e tcp.port -e frame.len > " + savePath
#         os.system(dumpCMD)
#         count += 1
#         print "Process Rate: " + str(count) + " / " + str(len(files))
