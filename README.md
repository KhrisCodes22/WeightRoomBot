# WeightRoomBot
This is a bot I have created to predict how many people will be at western's weight room on a particular day.
Steps are simple:
1) Use Selenium to pull past Tweets from the Western Weight Room twitter account (https://twitter.com/WesternWeightRm)
2) Clean the Twets to find the relevant information, and import it into a pandas dataframe
3) Using pandas and scikit-learn, perform regression to find an estimate of the number of people in the weight room at a given time and day
4) Evaluate accuracy of the model for that day.
