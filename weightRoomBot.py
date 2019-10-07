import tweepy as tw
import os
import pandas as pd
import matplotlib
import unicodedata
import re
import datetime
from datetime import datetime, timedelta
from selenium import webdriver
import csv
import timestring
import pickle
import sklearn



#driver = webdriver.Chrome(executable_path="C:\Users\Khris\Downloads\chromedriver_win32\chromedriver.exe")


#set up our API keys, and the dictionary where we store the data
#after we parse the csv and put the data into a dictionary, we create a pandas dataframe from the dictiontary
consumer_key= 'HPP2PKR3sGwyT57hwzqnwReHV'
consumer_secret= 'sSsHiym8YG4J0ZJeKLMwF3VLcY9BhxM3EseQww65SFJN9lhPBq'
access_token= '1176546248708501504-DVjS0pi9JepE8YptYzoKoUfnC4bfiQ'
access_token_secret= 'XmnXjbJWFCDfebugiFvel2RKiR6kML42cpWnCc50rs1pN'
auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)
workoutData = {"Calendar Day": [], "Date": [],  "WR":[], "CM":[]}
#subtract four hours from all dates because we want our date in the correct time zone
hoursToSubtract = 4


#function to round our time to the nearest half hour, to make all times uniform
#by default the function will round to the nearest half hour
def roundTime(dt = None, roundTo = 30*60):
    if dt == None: dt = datetime.datetime.now()
    seconds = (dt.replace(tzinfo=None) - dt.replace(hour = 0, minute = 0, second = 0)).seconds
    rounding = (seconds + roundTo / 2) // roundTo * roundTo
    return dt + timedelta(0, rounding - seconds, -dt.microsecond)


#function to add a new column that says "summer" if the date is in the summer where few students are at school
#will put "reading week" if university has a reading week during the date
#will put "none" if no breaks take place
def summerAndReadingWeek(dt):
    yearArray = [2015, 2016, 2017, 2018, 2019, 2020]
    for i in range(0, len(yearArray) - 1):
        winterStart = datetime(yearArray[i],12,21)
        winterEnd = datetime(yearArray[i+1], 1, 6)
        readingWeek1 = datetime(yearArray[i], 2, 17)
        readingWeek2 = datetime(yearArray[i], 2, 24)
        readingWeek3 = datetime(yearArray[i], 10, 7)
        readingWeek4 = datetime(yearArray[i], 10, 14)
        summerStart = datetime(yearArray[i], 4, 30)
        summerEnd = datetime(yearArray[i], 9, 4)
        if((dt > readingWeek1 and dt <readingWeek2) or (dt > readingWeek3 and dt < readingWeek4)):
            return("Reading Week")
        elif(dt > summerStart and dt < summerEnd):
            return("Summer Break")
        elif(dt > winterStart and dt < winterEnd):
            return("Winter Break")


#read in the csv file that has the tweets, and send it into a dictionary
def readCSV(fileToRead):
    with open(fileToRead) as file:
        readCSV = csv.reader(file, delimiter=',', dialect=csv.excel_tab)
        for row in readCSV:
            try:
                if(len(row) == 2):
                    textData = row[0]
                    timeData = row[1]
                    textDataSplit = textData.split(" ")
                    timeDataSplit = timeData.split(" ")
                    #check and see if tweet has been cleaned correctly
                    if((len(textDataSplit) == 4 or len(textDataSplit) == 5) and textDataSplit[0] == "WR"):
                        exactTime = datetime.strptime(timeData,"%a %b %d %H:%M:%S %Y")
                        #subtract 4 hours to put in correct time zone
                        exactTime = exactTime - timedelta(hours=hoursToSubtract)
                        workoutData["Date"].append(exactTime)
                        workoutData["WR"].append(textDataSplit[1])
                        workoutData["CM"].append(textDataSplit[3])
                        workoutData["Calendar Day"].append(timeDataSplit[0])
            except (IndexError, ValueError):
                continue
        print("{} has been read".format(fileToRead))


readCSV("westernweightrm.csv")
readCSV("newWeightData.csv")


#then create a pandas dataframe with this dictionary
workoutDF = pd.DataFrame.from_dict(workoutData)
#apply the rounding function
workoutDF["Date"] = workoutDF["Date"].apply(roundTime)
#print(workoutDF.head(25))
workoutDF["Special Days"] = workoutDF["Date"].apply(summerAndReadingWeek)
#check to make sure it works
print(workoutDF.head(25))


#save the csv file
workoutDF.to_pickle("allWorkoutData.pkl")


