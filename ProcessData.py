# THRs: 
# 1. n 個 time intervals
# 2. 每個 time interval 的 client 數量
# 3. 與前一個 time interval 的 client 交集 數量

# ACs:
# 1. n 個 time intervals
# 2. 每個 time interval 的 client 數量

# PSSs:
# 1. 每個 time interval 中, 最大的 response payload
# 2. ACs

import os
import re
import datetime
from datetime import timedelta