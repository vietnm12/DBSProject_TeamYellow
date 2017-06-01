# -*- coding: utf-8 -*-
import csv
import re
#suche nach den #Keyword, Datum und Zeit mit RE
find_hashtags =re.compile("#[A-Za-z0-9]+").findall
find_date =re.compile("[0-9]+-[0-9]+-[0-9]+").findall
find_time =re.compile("[0-9]+:[0-9]+:[0-9]+").findall
#öffnen der Dateien fürs Lesen und Schreiben
with open('new.csv', 'wb') as newcsv:
    csvfile = open("american-election-tweets2.csv", "rb")
    reader = csv.DictReader(csvfile.read().decode('utf-8-sig').encode('utf-8').splitlines(), delimiter=';')
    fieldnames = ['tweet_id','owner_name','owner_id', 'tweet_content','original_author', 'tweet_time','tweet_date', 'in_reply_to_screen_name',
                    'retweet_count', 'favorite_count', 'hashtag','hashtag_id']
    writer = csv.DictWriter(newcsv, fieldnames=fieldnames, delimiter=';')
    writer.writeheader()
    all_keywords=[]
    count=0
    for row in reader:
        count+=1
        #suche keywords, zeit und datum
        keywords = list(map(str.lower, find_hashtags(row['text'])))
        zeit = find_time(row['time'])
        datum = find_date(row['time'])
        owner_id=2
        if row['handle']=='HillaryClinton':
            owner_id=1
        i=0
        if keywords!=[]:
           while i <(len(keywords)-1):
               i+=1
               # Liste alle Hashtags (distinct) erstellen, um dann den Index zu vergeben
               if keywords[i] not in all_keywords:
                   all_keywords.append(keywords[i])
                #Daten in die Datei schreiben, falls Hashtag gefunden wurde
               writer.writerow({'tweet_id':count, 'owner_name': row['handle'],'owner_id':owner_id, 'tweet_content': row['text'],
                             'original_author': row['original_author'],
                             'tweet_time': zeit[0],'tweet_date':datum[0], 'in_reply_to_screen_name': row['in_reply_to_screen_name'],
                             'retweet_count': row['retweet_count'],
                             'favorite_count': row['favorite_count'], 'hashtag': keywords[i],'hashtag_id':all_keywords.index(keywords[i])})
        else:
            #Daten in die Datei schreiben(ohne Hashtag)
            writer.writerow({'tweet_id':count, 'owner_name': row['handle'],'owner_id':owner_id, 'tweet_content': row['text'],
                             'original_author': row['original_author'],'tweet_time': zeit[0],'tweet_date':datum[0], 'in_reply_to_screen_name': row['in_reply_to_screen_name'],
                             'retweet_count': row['retweet_count'],'favorite_count': row['favorite_count'], 'hashtag': ''})
        keywords = []