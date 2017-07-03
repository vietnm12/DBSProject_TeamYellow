# -*- coding: utf-8 -*-
"""
Created on Sat Jul  1 10:18:11 2017

@author: Duong
"""

import pandas as pd
import matplotlib.pyplot as plt
import psycopg2
from pandas.core.frame import DataFrame





# DBS verbinden
database = psycopg2.connect(database="TeamYellow_election", user="student", password="password", host="agdbs-edu01.imp.fu-berlin.de", port="5432")

# SQl-Abfrage
cursor = database.cursor()
cursor.execute(
    'SELECT tweet_date, COUNT(*) FROM projekt_election.tweet as tweet , projekt_election.hashtag_use as use WHERE tweet.tweet_id = use.tweet_id GROUP BY tweet_date ORDER BY tweet_date ASC')
result = cursor.fetchall()

# Dataframe erstellen
data=DataFrame(result, columns=['tweet_date', 'count'])


#Umwandlung des Datentyp der Spalte tweet_date
data['tweet_date_with_time'] = data['tweet_date'].astype('datetime64[ns]')
data['week_number'] = data['tweet_date_with_time'].dt.week
data['weekday']= data['tweet_date_with_time'].dt.dayofweek


# Gruppierung der Kalendarwochen mit einzelnen Counts
data2=data.copy()
del data2['tweet_date']
del data2['tweet_date_with_time']
del data2['weekday']

print(data2.groupby('week_number')['count'].apply(list))

# Aufbau Dataframe auf Erkenntnisse aus data2-Prints
data3 = pd.DataFrame({'KW01':            [0, 0, 1, 0, 3, 0, 0],
                     'KW02':            [3, 1, 7, 1, 0, 1, 0],
                     'KW03':            [0, 2, 6, 1, 11, 3, 2],
                     'KW04':            [13, 5, 1, 3, 6, 2, 1],
                     'KW05':            [0, 1, 2, 0, 4, 3, 4],
                     'KW06':            [2, 6, 1, 2, 1, 5, 0],
                     'KW07':            [1, 3, 5, 2, 5, 2, 1],
                     'KW08':            [2, 7, 1, 3, 5, 1, 3],
                     'KW09':            [3, 10, 9, 3, 3, 6, 2],
                     'KW10':           [0, 1, 2, 0, 2, 4, 0],
                     'KW11':           [2, 3, 8, 0, 3, 10, 5],
                     'KW12':           [0, 11, 4, 1, 0, 0, 0],
                     'KW13':           [1, 0, 3, 2, 1, 6, 5],
                     'KW14':           [4, 5, 0, 0, 1, 1, 2],
                     'KW15':           [2, 4, 1, 2, 0, 4, 2],
                     'KW16':           [0, 11, 4, 2, 3, 4, 1],
                     'KW17':           [2, 6, 0, 1, 1, 0, 0],
                     'KW18':           [4, 8, 0, 1, 1, 0, 0],
                     'KW19':           [2, 8, 3, 0, 0, 0, 0],
                     'KW20':           [1, 1, 1, 0, 5, 0, 1],
                     'KW21':           [0, 0, 2, 1, 1, 0, 0],
                     'KW22':           [0, 0, 1, 4, 2, 3, 0],
                     'KW23':           [0, 0, 1, 0, 1, 2, 0],
                     'KW24':           [0, 0, 3, 0, 1, 4, 1],
                     'KW25':           [0, 0, 1, 10, 0, 0, 0],
                     'KW26':           [1, 1, 0, 0, 2, 3, 0],
                     'KW27':           [1, 0, 0, 2, 0, 0, 0],
                     'KW28':           [1, 2, 2, 1, 0, 1, 0],
                     'KW29':           [0, 1, 2, 7, 2, 1, 0],
                     'KW30':           [1, 3, 3, 4, 0, 1, 1],
                     'KW31':           [3, 2, 2, 0, 1, 4, 1],
                     'KW32':           [1, 6, 0, 0, 0, 1, 0],
                     'KW33':           [0, 0, 4, 0, 1, 1, 0],
                     'KW34':           [1, 0, 1, 2, 1, 2, 1],
                     'KW35':           [2, 0, 1, 3, 1, 0, 0],
                     'KW36':           [1, 1, 2, 2, 2, 0, 0],
                     'KW37':           [0, 1, 1, 2, 4, 0, 0],
                     'KW38':           [0, 3, 0,  2, 1, 1, 0],
                     'KW39':           [3, 18, 0, 0, 0, 0, 0]})


data4= data3.transpose()
data4.columns =['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']
data4['Kalendarwoche']=data4.index

#############################   Bau eines Stacked Bar Chart ############################################

#Grundgerüst des Balkendiagramms
f, ax1 = plt.subplots(1, figsize=(25,20))

# Balkengröße
bar_width = 0.75

# Balken fangen von links an
bar_l = [i+1 for i in range(len(data4['Montag']))]

# Position der X-Achsen Werte
tick_pos = [i+(bar_width/2) for i in bar_l]

# Beginn der Erstellung der Balken nach Wochentagen
ax1.bar(bar_l,
        data4['Montag'],
        width=bar_width,
        label='Montag',
        alpha=0.5,
        color='#1858ef')


ax1.bar(bar_l,
        data4['Dienstag'],
        width=bar_width,
        bottom=data4['Montag'],
        label='Dienstag',
        alpha=0.5,
        color='#6618ef')

ax1.bar(bar_l,
        data4['Mittwoch'],
        width=bar_width,
        bottom=[i+j for i,j in zip(data4['Montag'],data4['Dienstag'])],
        label='Mittwoch',
        alpha=0.5,
        color='#ef1829')

ax1.bar(bar_l,
        data4['Donnerstag'],
        width=bar_width,
        bottom=[i+j+k for i,j,k in zip(data4['Montag'],data4['Dienstag'], data4['Mittwoch'])],
        label='Donnerstag',
        alpha=0.5,
        color='#ef7c18')

ax1.bar(bar_l,
        data4['Freitag'],
        width=bar_width,
        bottom=[i+j+k+l for i,j,k,l in zip(data4['Montag'],data4['Dienstag'], 
                                           data4['Mittwoch'], data4['Donnerstag'])],
        label='Freitag',
        alpha=0.5,
        color='#efc718')

ax1.bar(bar_l,
        data4['Samstag'],
        width=bar_width,
        bottom=[i+j+k+l+m for i,j,k,l,m in zip(data4['Montag'],data4['Dienstag'], 
                                           data4['Mittwoch'], data4['Donnerstag'], data4['Freitag'])],
        label='Samstag',
        alpha=0.5,
        color='#63ef18')


ax1.bar(bar_l,
        data4['Sonntag'],
        width=bar_width,
        bottom=[i+j+k+l+m+n for i,j,k,l,m,n in zip(data4['Montag'],data4['Dienstag'], 
                                           data4['Mittwoch'], data4['Donnerstag'], data4['Freitag'],
                                           data4['Samstag'])],
        label='Sonntag',
        alpha=0.5,
        color='#18efa3')

# X-Achse mit Werte versehen
plt.xticks(tick_pos, data4['Kalendarwoche'])

#Legende
ax1.set_ylabel("Häufigkeit")
ax1.set_xlabel("Kalendarwoche")
plt.legend(loc='upper left')

# Zwischen den Diagrammen Platz lassen
plt.xlim([min(tick_pos)-bar_width, max(tick_pos)+bar_width])

############### Balkendiagramm nach Kalendarwoche#########################################

kw = lambda x: x.isocalendar()[1]
grouped = data.groupby([data['tweet_date_with_time'].map(kw)], sort=False).agg({'count': 'sum'})

grouped['calendar week']= ('KW1','KW2','KW3','KW4','KW5','KW6','KW7','KW8','KW9','KW10','KW11','KW12','KW13',
               'KW14','KW15','KW16','KW17','KW18','KW19','KW20','KW21','KW22','KW23','KW24','KW25','KW26', 'KW27','KW28','KW29',
               'KW30','KW31','KW32','KW33','KW34','KW35','KW36','KW37','KW38','KW39')



#Balkendiagramm für alle Hashtag in Kalendarwoche
grouped.set_index('calendar week').plot.bar(rot=45, title='Nutzung von #makeamericagreatagain in Kalendarwoche', figsize=(15,10), fontsize=10)

############## Balkendiagramm für alle Hashtag pro Tag #####################################
data5=data[['tweet_date','count']].copy()
#Balkendiagramm für alle Hashtag in Tagen
data5.set_index('tweet_date').plot.bar(rot=90, title='Häufigkeit aller Hashtag in Tagen', figsize=(50,25), color ='#ef6618', fontsize=14)

