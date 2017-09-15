import os

count = 0
filePath = "/home/wmlab/Desktop/ISOT_Botnet_DataSet_2010/splited/"
for root, dirs, files in os.walk(filePath):
    print root
    for name in files:
        path = os.path.join(root, name)
        savePath = "/home/wmlab/Desktop/ISOT_Botnet_DataSet_2010/isotCSV/" + name + ".csv"
        cmd = "tshark -r " + path + " -T fields -e frame.time -e _ws.col.Protocol -e ip.src -e ip.dst -e tcp.port -e frame.len > " + savePath
        os.system(cmd)
        count += 1
        print "Process Rate: " + str(count) + " / " + str(len(files))
