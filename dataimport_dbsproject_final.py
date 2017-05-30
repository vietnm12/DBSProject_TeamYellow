import psycopg2
import csv

# Lesen der CSV-Dateien
account_owner_data = csv.reader(open('account_owner.csv', 'r'), delimiter=';')

tweet_data = csv.reader(open('tweet.csv', 'r'), delimiter=';')

hashtag_data = csv.reader(open('hashtag.csv', 'r'), delimiter=';')

hashtag_use_data = csv.reader(open('hashtag_use.csv', 'r'), delimiter=';')

# Verbindung mit der Datenbank
database = psycopg2.connect(database="TeamYellow_election", user="student", password="password", host="agdbs-edu01.imp.fu-berlin.de", port="5432")

cursor = database.cursor()

# 1. Zeile der CVS-Datei überspringen
next(account_owner_data)
next(tweet_data)
next(hashtag_data)
next(hashtag_use_data)

# Daten der CSV_Dateien werden in die Tabellen der Datenbank importiert
for row in account_owner_data:
    cursor.execute("INSERT INTO projekt_election.account_owner (owner_id, owner_name) VALUES (%s, %s);", row)
for row in tweet_data:
    cursor.execute("INSERT INTO projekt_election.tweet (owner_id, tweet_id, tweet_content, in_reply_to, org_author, retweet_count, favorite_count, tweet_date, tweet_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;", row)
for row in hashtag_data:
    cursor.execute("INSERT INTO projekt_election.hashtag (hashtag_id, hashtag_name) VALUES (%s, %s);", row)
for row in hashtag_use_data:
    cursor.execute("INSERT INTO projekt_election.hashtag_use (tweet_id, hashtag_id) VALUES (%s, %s);", row)

cursor.close()
database.commit()
database.close()

print("CSV-Dateien importiert")
