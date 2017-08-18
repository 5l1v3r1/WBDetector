

# start from startStamp, split each IP by hour
# create dict by timestamp
def SplitByHour(serverDict):
    
    for server in serverDict:
        startStamp = datetime.datetime.strptime("2017-03-01 00:00:00.000", "%Y-%m-%d %H:%M:%S.%f")
        for data in server.keys():
            for row in data:
                if (row.get('Date flow start') - startStamp) < timedelta(hours = 1):
                    
                else:
                    firstInHour = True


    pass





