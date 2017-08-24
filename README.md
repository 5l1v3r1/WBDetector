# WBDetector
implement Detecting Web-based Botnets Using Bot Communication Traffic Features

## NetFlow Data
檔案依時間排序，但同一 time stamp 可能出現在不同檔案中
1. 預處理 csv 檔, 不完整的 row data 就丟掉,  
=> return dataList [{}]...[{}]

2. 挑出 port number 為 443 或 8080 的, 分成 Src 與 Dst, 依照 IP 排序,  
=> return serverList[srcList, dstList]

3. 把 serverList 依照 IP 建立 dict  
=> return serverDict{serverIP, srcList}, serverDict{serverIP, dstList}

4. 訂定一個開始時間(兩 serverDict 才會從一樣的地方開始), 資料每隔一小時切開一次  
=> return srcDict{IP: timeDict{timeInterval:[srcList]}}, dstDict{IP: timeDict{timeInterval:[dstList]}}

### 一條龍式作法, 產生 Memory Error
每個檔案都先做 step 1~3, 合併起來再去 step4 切 timeInterval,
可先拿去白色主機跑看看, 並思考如何切開可省下記憶體

## Formula Parameter
### THRs: 
1. n 個 time intervals
2. 每個 time interval 的 client 數量
3. 與前一個 time interval 的 client 交集 數量

### ACs:
1. n 個 time intervals
2. 每個 time interval 的 client 數量

### PSSs:
1. 每個 time interval 中, 最大的 response payload
2. ACs
