# -*- coding: utf-8 -*-

import psycopg2
from pandas.core.frame import DataFrame

# DBS connect
database = psycopg2.connect(database="TeamYellow_election", user="student", password="password", host="agdbs-edu01.imp.fu-berlin.de", port="5432")

# SQl execution
cursor = database.cursor()
cursor.execute(
    'select hst.hashtag_name, hstu.tweet_id, hstu.hashtag_id from projekt_election.hashtag_use hstu, projekt_election.hashtag hst where hstu.hashtag_id=hst.hashtag_id order by hstu.hashtag_id')
result = cursor.fetchall()

# put data into CSV file
df=DataFrame(result, columns=['hashtag', 'tweet_id', 'hashtag_id'])
df.to_csv('tweet.csv')

