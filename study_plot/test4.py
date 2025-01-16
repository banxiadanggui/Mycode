import json
import math
import matplotlib.pyplot as plt

filename='btc_close_urllib.json'
with open(filename) as f:
    btc_data=json.load(f)
date,month,week,weekday,close=[],[],[],[],[]
for btc_dict in btc_data:
    date.append(btc_dict['date'])
    month.append(int(btc_dict['month']))
    week.append(int(btc_dict['week']))
    weekday.append(btc_dict['weekday'])
    close.append(int(float(btc_dict['close'])))
major_date=date[::20]
major_close=[math.log10(_) for _ in close[::20]]
fig=plt.figure(dpi=128,figsize=(10,6))
plt.plot(major_date,major_close,c='black')
plt.title("map",fontsize=20)
plt.xlabel("time",fontsize=20)
plt.ylabel("price",fontsize=20)
fig.autofmt_xdate()
plt.show()