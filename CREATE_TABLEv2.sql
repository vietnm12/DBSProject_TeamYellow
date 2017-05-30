CREATE SCHEMA projekt_election;
CREATE TABLE projekt_election.account_owner(owner_id INT PRIMARY KEY, 
                           owner_name CHAR(80) NOT NULL);
CREATE TABLE projekt_election.tweet(owner_id INT REFERENCES projekt_election.account_owner(owner_id),
                   tweet_id INT PRIMARY KEY,
                   tweet_content TEXT NOT NULL,
                   in_reply_to CHAR(80),
                   org_author CHAR (80),
                   retweet_count INT CHECK (retweet_count >= 0) NOT NULL,
                   favorite_count INT CHECK (favorite_count >= 0) NOT NULL,
                   tweet_date date,
                   tweet_time time);
 
CREATE TABLE projekt_election.hashtag(hashtag_id INT PRIMARY KEY, 
                     hashtag_name CHAR(80)NOT NULL);

CREATE TABLE projekt_election.hashtag_use(tweet_id INT, hashtag_id INT, PRIMARY KEY(tweet_id, hashtag_id));