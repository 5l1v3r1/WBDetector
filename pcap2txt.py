import os

fileDir = "/home/wmlab/Desktop/Botnet_Dataset/Sality/splited/"
saveDir = "/home/wmlab/Desktop/Botnet_Dataset/Sality/extract/"

if not os.path.exists(saveDir):
	os.mkdir(saveDir)

for root, dirs, files in os.walk(fileDir):
    print root
    count = 0
    for name in files:
        path = os.path.join(root, name)
        savePath = saveDir + name + ".txt"
        cmd = "tshark -r " + path + " -T fields -e frame.time -e _ws.col.Protocol -e ip.src -e ip.dst -e tcp.port -e frame.len > " + savePath
        os.system(cmd)
        count += 1
        print "Process Rate: " + str(count) + " / " + str(len(files))
