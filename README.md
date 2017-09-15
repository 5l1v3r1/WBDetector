# WBDetector
implement Detecting Web-based Botnets Using Bot Communication Traffic Features

## NetFlow Data
檔案依時間排序，但同一 time stamp 可能出現在不同檔案中
1. 預處理 csv 檔, 不完整的 row data 就丟掉,  
=> return dataList [{}...{}]

2. 挑出 Source 的 port number 為 443 或 8080 的, 依照 IP 排序,  
=> return serverList[{}...{}]

3. 把 serverList 依照 IP 建立 dict  
=> return serverDict{serverIP, srcList}

4. 訂定一個開始時間(兩 serverDict 才會從一樣的地方開始), 資料每隔一小時切開一次  
=> return srcDict{IP: timeDict{timeInterval:[srcList]}}}

### 一條龍式作法, 產生 Memory Error
每個檔案都先做 step 1~3, 合併起來再去 step4 切 timeInterval,  
可先拿去白色主機跑, 但記憶體還是不夠用, 一條龍可能不適合

### 做部分資料整理後, 先存檔備用
每個檔案都先做 step 1~3, 依照 IP 存成 txt 檔, 再去 step4 切 timeInterval,  
再個別從每個檔案取出所需參數, 完成計算

## Formula Parameter
### THRs: 
1. n 個 time intervals
2. 每個 time interval 的 client 數量
3. 與前一個 time interval 的 client 交集 數量

### ACs:
1. n 個 time intervals
2. 每個 time interval 的 client 數量

### PSSs:
1. 每個 time interval 中, 最大的 payload
2. ACs

## ISOT Dataset
ISOT.pcap 用 nfdump 出現 bad magic error, 但用 wireshark 開得起來
因檔案過大. wireshark 要開很久, 所以用
tcpdump -r ISOT_Botnet_DataSet_2010.pcap -w newfiles -C 10
將原始檔案切成每個 10MB 的檔案, 共切出了 1140 個檔案
再用 tshark 將檔案取出需要欄位後, 倒入 csv 檔
