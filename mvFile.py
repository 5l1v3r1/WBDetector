

import os

cmd = 'newfiles11[0-9][0-9]$'
arr = os.popen( "ls | grep " + cmd ).read()

arr = arr.split()


os.system("mkdir 12")

path = "./12/"
for name in arr:
    print name
    os.system( "mv ./" + name + " " + path )
