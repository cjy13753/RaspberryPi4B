import Adafruit_DHT as dht
import time
from datetime import datetime
import pymysql
import os

list_hum = []
list_temp = []
for i in range(5):
    try:
        hum,temp = dht.read_retry(dht.DHT11, 4)
    except:
        pass
    if hum is not None:
        list_hum.append(hum)
    if temp is not None:
        list_temp.append(temp)
    time.sleep(1)
avg_hum = sum(list_hum)/len(list_hum)
avg_temp = sum(list_temp)/len(list_temp)

# format = "%Y-%m-%d %H-%M-%S %Z"
# print("time:{}, temperature: {:.1f}, humidity: {:.1f}".format(datetime.now(timezone('Asia/Seoul')).strftime(format),avg_temp, avg_hum))

conn = pymysql.connect(host=os.environ.get('AWS_RDS_MYSQL_HOST'), user='admin', password=os.environ.get('AWS_RDS_MYSQL_PASSWORD'), db='humidity')
cur = conn.cursor()
query = 'INSERT INTO room_condition VALUES (%s, %s, %s)'
cur.execute(query, (datetime.now(), avg_temp, avg_hum))
conn.commit()
cur.close()
conn.close()