#!/usr/bin/env python
# coding: utf-8


#Importing the necessary packages

import numpy as np
from flask import Flask, request, jsonify, render_template
from textblob import TextBlob
import sys, tweepy
import matplotlib.pyplot as plt

# The first step is loading the flask ibrary and creating a flask object using the name special variable

app = Flask(__name__)

#Creating a function to evaluate the percentage of various polarities

def percentage(part, whole):
  return 100 * float(part)/float(whole)

#Creating the route for the web application to connet with the front end using the html index.html file
@app.route('/')
def home():
    return render_template('index.html')

# We define the predict function with flask annotation that specifies that the function should be hosted at "/" 
# and should be accesible by HTTP GET and POST commands

@app.route('/predict',methods=["POST","GET"])
def predict():

# Connecting the results to the HTML GUI    
    int_features = [x for x in request.form.values()]
    final_features = [np.array(int_features)]
    
# Adding the Twitter Developer account credentials to variables 
    consumerKey = "c4cK1xqfC3MocKF4gPwE0vHFH"
    consumerSecret = "s6T5kM503GQ49mE2ZRNNUtz7VRTNCqHsox1gVOPRFmSv5CHwSV"
    accessToken = "1244402689175420929-BilxLAuVQotLB4HMAWuECgnuCQewmY"
    accessTokenSecret = "sm8ygnOT7Xzjb2iaZL95yR5oPWpJQKIwu7PNgBs8BOnRJ"

# Obtaining the authorisation for Twitter API to be able to stream the tweets
    auth =tweepy.OAuthHandler(consumer_key=consumerKey, consumer_secret=consumerSecret)
    auth.set_access_token(accessToken, accessTokenSecret)
    api= tweepy.API(auth)

# Streaming the tweets
    tweets=tweepy.Cursor(api.search, q=final_features[0][0], language="English").items(int(final_features[0][1]))
    noOfSearchTerms=int(final_features[0][1])
    positive=0
    negative=0
    neutral=0
    polarity=0

# Iterating through the tweets and analyzing the polarities
  
    for tweet in tweets:
      analysis=TextBlob(tweet.text)
      polarity+=analysis.sentiment.polarity
      
      if(analysis.sentiment.polarity == 0):
        neutral+=1
      elif(analysis.sentiment.polarity < 0):
        negative+=1
      elif(analysis.sentiment.polarity > 0):
        positive+=1
    positive=percentage(positive, noOfSearchTerms)
    negative=percentage(negative, noOfSearchTerms)
    neutral=percentage(neutral, noOfSearchTerms)
    polarity=percentage(polarity,noOfSearchTerms)

    positive=format(positive,'0.2f')
    negative=format(negative,'0.2f')
    neutral=format(neutral,'0.2f')

# Evaluating the polarity of the topic   
    if(polarity == 0.00):
      output="Neutral"
    elif(polarity < 0.00):
      output="Negative"
    elif(polarity > 0.00):
      output="Positive"

# Returning the final overall sentiment to the front end
    return render_template('index.html', prediction_text='Overall Sentiment : {}'.format(output))


if __name__ == "__main__":
    app.run(host='0.0.0.0')




