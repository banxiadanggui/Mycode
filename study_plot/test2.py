import csv
from datetime import datetime
from matplotlib import pyplot as plt

filename='sitka_weather_2014.csv'
with open(filename) as x: 
    reader=csv.reader(x)
    header_row=next(reader)
    
    high,low=[],[]
    date=[]
    for row in reader:
        current_date=datetime.strptime(row[0],"%Y-%m-%d")
        date.append(current_date)
        high.append(int(row[1]))
        low.append(int(row[3]))
    
    fig =plt.figure(dpi=128,figsize=(10,6))
    plt.plot(date,high,c='red')
    plt.plot(date,low,c='blue')
    plt.fill_between(date,high,low,facecolor='blue',alpha=0.1)
    fig.autofmt_xdate()
    plt.title("Daily high temperatures,July 2024",fontsize=24)
    plt.xlabel('',fontsize=16)
    plt.ylabel('Temperatue(F)',fontsize=16)
    plt.tick_params(axis='both',which='major',labelsize=16)

    plt.show()