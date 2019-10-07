import tweepy
import json
import math
import glob
import csv
import zipfile
import zlib
from tweepy import TweepError
from time import sleep
import sys
import datetime
from datetime import timedelta
import re
import pandas as pd
# encoding = utf-8

# SET TO TWITTER USER YOU WANT
user = 'WesternWeightRm'

with open('api_keys.json') as f:
    keys = json.load(f)

#authenticate with twitter api
auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
auth.set_access_token(keys['access_token'], keys['access_token_secret'])
api = tweepy.API(auth)
user = user.lower()

#open ids of tweets to pull
with open('all_ids.json') as f:
    ids = json.load(f)

print('total ids: {}'.format(len(ids)))


#list to store content of tweets
tweet_data = []
#list to store times of tweets
time_data = []
start = 0
end = 100
limit = len(ids)
i = int(math.ceil(limit / 100))
if limit < 100: i = 1

for go in range(i):
    print('currently getting {} - {}'.format(start, end))
    sleep(6)  # needed to prevent hitting API rate limit
    id_batch = ids[start:end]
    start += 100
    end += 100
    tweets = api.statuses_lookup(id_batch)
    for tweet in tweets:
        tweet_data.append(tweet.text)
        time_data.append(tweet.created_at)

#function to clean the text of the tweet, using regularexpressions
def cleanTweet(tweetString):
    tweetString = re.sub("Cardio", "CM", tweetString)
    tweetString = re.sub(r"(WR|wr|CM|cm|Wr|Cm)(\d+)", r"\1 \2", tweetString)
    #reverse the format
    tweetString = re.sub(r"^(\d+)\s+(WR|wr)\s+(\d+)\s+(CM|cm)", r"\2 \1 \4 \3", tweetString)
    tweetString = re.sub(r"^(\d+)\s+(CM|cm)\s+(\d+)\s+(WR|wr)", r"\4 \3 \2 \1", tweetString)
    #remove everything that is not a CM or WR or number
    tweetString = re.sub(r"[^WR|wr|CM|cm|\d|\s]", "", tweetString)
    tweetString = re.sub(" m", "", tweetString)
    return tweetString

dataDict = {}
#now take all_data and clean the data, using the cleanTweet function
#after the tweet is cleaned, store the tweet in the csv.
fields = ["text", "created_at"]
csvFile = csv.writer(open('newWeightData.csv', 'w'))
csvFile.writerow(fields)
for x in range(0,len(tweet_data)):
    tweetText = tweet_data[x].encode("utf-8", "ignore")
    cleanedText = cleanTweet(tweetText)
    textArray = cleanedText.split(" ")
    newRow = [cleanedText, time_data[x]]
    csvFile.writerow(newRow)

#create dataframe from csv
newDF = pd.read_csv('newWeightData.csv')
print(newDF.head())