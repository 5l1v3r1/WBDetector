import os
import csv
import time

    
    def readRecordFile(self, record_path):
        with open(record_path,"r") as csvfile:
            for row in csv.reader(csvfile):
                self.flowdata.append(row[0])
        self.flowdata.pop(0)

    def changeFlowdataToDictSet(self, rules):
        dict_set = []

        for row in self.flowdata:
            value = row.split(" ")       
            value = filter(lambda i:i!='',value)
            print value
        
            value  = self.restructureValue(value, rules)
            
            if self.ignore_flag == True:
                self.ignore_flag = False
                continue
            row_item = self.makeDictFormat(value)
            dict_set.append(row_item)

        return dict_set

    def restructureValue(self, value, rules):
        new_value = ['' for i in range(len(self.key_list))]
        dateStr = ""
        #print value
        if len(value) != len(rules):
            # repair structure
            value = self.repairValueStructure(value)
            if self.ignore_flag == True:
                return
        for i in range(len(value)):
            if rules[i] > 0:
                new_value[rules[i]] = value[i]
            elif rules[i] == 0:
                dateStr += value[i]+" "
            elif rules[i] == -1:
                ipport = value[i].split(':')
                new_value[i-1] = ipport[0]
                new_value[i] = ipport[1]
        new_value[0] = dateStr
        return new_value

    def makeDictFormat(self, value):
        row_item = list(zip(self.key_list, value))
        row_item = dict(row_item)
        return row_item
    
    def repairValueStructure(self, value):
        if len(value) == 11 and self.checkUnit(value, 9):
            byte_value = value.pop(8)
            byte_unit = value.pop(8)
            value.insert(8,byte_value+byte_unit)
            #print value
        elif len(value) == 12 and self.checkUnit(value, 8) and self.checkUnit(value,10):
            packet_value = value.pop(7)
            packet_unit  = value.pop(7)
            byte_value   = value.pop(7)
            byte_unit    = value.pop(7)
            value.insert(7,packet_value+packet_unit)
            value.insert(8,byte_value+byte_unit)
            print value
        elif len(value) < 10:
            self.ignore_flag = True
        elif len(value) > 12:
            print value
        return value

    def checkUnit(self, value, pos):
        return value[pos]=='M' or value[pos]=='G' or value[pos]=='K'


if __name__ == '__main__':
    parser = DataPreprocess()
    record_path = "/home/joe/flowlog/record"
    rules = {0:0, 1:0, 2:1, 3:2, 4:-1, 5:-2 ,6:-1, 7:7, 8:8, 9:9}
    
    t1 = time.clock()
    record_files = os.listdir(record_path)
    
    for filename in record_files:
        path = record_path +"/"+filename
        parser.readRecordFile(path)
        FileDictSet = parser.changeFlowdataToDictSet(rules)
        #break
        parser.flowdata = []
        print len(FileDictSet)
        print "."
        break
    #print FileDictSet[22]
    #print len(FileDictSet)
    t2 = time.clock()
    print "cost {0} sec".format(t2-t1)
 
