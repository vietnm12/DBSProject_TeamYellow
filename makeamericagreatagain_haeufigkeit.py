# -*- coding: utf-8 -*-
"""
Created on Sat Jul  1 22:12:11 2017

@author: Duong
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import pyplot as plt
import psycopg2
from pandas.core.frame import DataFrame




# DBS verbinden
database = psycopg2.connect(database="TeamYellow_election", user="student", password="password", host="agdbs-edu01.imp.fu-berlin.de", port="5432")

# SQl-Abfrage
cursor = database.cursor()
cursor.execute(
    'SELECT n.tweet_date, COUNT(*) FROM projekt_election.tweet as n JOIN projekt_election.hashtag_use as u ON n.tweet_id = u.tweet_id JOIN projekt_election.hashtag as h ON h.hashtag_id = u.hashtag_id WHERE h.hashtag_id = 0 GROUP BY n.tweet_date ORDER BY n.tweet_date ASC')
result = cursor.fetchall()

# Dataframe erstellen
data=DataFrame(result, columns=['tweet_date', 'count'])

database = psycopg2.connect(database="TeamYellow_election", user="student", password="password", host="agdbs-edu01.imp.fu-berlin.de", port="5432")

# SQl-Abfrage
cursor = database.cursor()
cursor.execute(
    'SELECT n.tweet_date, COUNT(*) FROM projekt_election.tweet as n JOIN projekt_election.hashtag_use as u ON n.tweet_id = u.tweet_id JOIN projekt_election.hashtag as h ON h.hashtag_id = u.hashtag_id WHERE h.hashtag_id = 0 GROUP BY n.tweet_date ORDER BY n.tweet_date ASC')
result = cursor.fetchall()

# Dataframe erstellen
data=DataFrame(result, columns=['tweet_date', 'count'])


data['tweet_date_with_time'] = data['tweet_date'].astype('datetime64[ns]')

# Datum nach der Kalendarwoch zusammenfassen
kw = lambda x: x.isocalendar()[1]
grouped = data.groupby([data['tweet_date_with_time'].map(kw)], sort=False).agg({'count': 'sum'})

grouped['calendar week']= ('KW1','KW2','KW3','KW4','KW5','KW6','KW7','KW8','KW9','KW10','KW11','KW12','KW13',
               'KW14','KW15','KW16','KW18','KW19','KW20','KW21','KW22','KW29','KW36','KW38','KW39',)



#Balkendiagramm für alle Hashtag in Kalendarwoche
grouped.set_index('calendar week').plot.bar(rot=45, title='Nutzung von #makeamericagreatagain in Kalendarwoche', figsize=(15,10), fontsize=10)

##Balkendiagramm für alle Hashtag in Tagen
data.set_index('tweet_date').plot.bar(rot=90, title='Nutzung von #makeamericagreatagain in Tagen', figsize=(15,10), fontsize=8)
