import Adafruit_DHT as dht
import time
from datetime import datetime
import pymysql
import os
import pandas as pd

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

moisture_table = pd.read_csv('~/Desktop/Projects/Hygrometer/temp_moisture.csv', header=0)
mois_max_in_m3 = list(moisture_table.loc[moisture_table['temperature']==avg_temp, 'max_moisture'])[0]
mois_real_in_m3 = round(mois_max_in_m3 * avg_hum / 100, 1)

conn = pymysql.connect(host=os.environ.get('AWS_RDS_MYSQL_HOST'), user='admin', password=os.environ.get('AWS_RDS_MYSQL_PASSWORD'), db='humidity')
cur = conn.cursor()
query = 'INSERT INTO room_condition VALUES (%s, %s, %s, %s)'
cur.execute(query, (datetime.now(), avg_temp, avg_hum, mois_real_in_m3))
conn.commit()
cur.close()
conn.close()