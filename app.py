#Importing the necessary packages

import numpy as np
from flask import Flask, request, jsonify, render_template
from textblob import TextBlob
import sys, tweepy
import matplotlib.pyplot as plt

app = Flask(__name__)

#Creating a function to calculate the percentage of polarities for tweets

def percentage(part, whole):
  return 100 * float(part)/float(whole)

#Creating a route for the web app to connect to the front end using the index.html file
@app.route('/')
def home():
    return render_template('index.html')

#Note, we dont specify the path because the html file is in the same folder

@app.route('/predict',methods=['POST'])
def predict():

# Connecting the results with HTML GUI    
    int_features = [x for x in request.form.values()]
    final_features = [np.array(int_features)]
    

# Assigning the Twitter Developer Account creadentials to  variables
    consumerKey="c4cK1xqfC3MocKF4gPwE0vHFH"
    consumerSecret="s6T5kM503GQ49mE2ZRNNUtz7VRTNCqHsox1gVOPRFmSv5CHwSV"
    accessToken="1244402689175420929-BilxLAuVQotLB4HMAWuECgnuCQewmY"
    accessTokenSecret="sm8ygnOT7Xzjb2iaZL95yR5oPWpJQKIwu7PNgBs8BOnRJ"
    
# Note: It is a pre-requisite to have these credentials. These credentials belong to nikhita wadhawan.

# Obtaining authorisation to connect to twitter API 
    auth =tweepy.OAuthHandler(consumer_key=consumerKey, consumer_secret=consumerSecret)
    auth.set_access_token(accessToken, accessTokenSecret)
    api= tweepy.API(auth)

# Extracting the tweets
    tweets=tweepy.Cursor(api.search, q=final_features[0][0], language="English").items(int(final_features[0][1]))
    SearchTerms=int(final_features[0][1])
    positive=0
    negative=0
    neutral=0
    polarity=0
    
# Note: we are only using the tweets that are in english language  

# Iterating through tweets to analyse the polarities
    for tweet in tweets:
      analysis=TextBlob(tweet.text)
      polarity+=analysis.sentiment.polarity
      
      if(analysis.sentiment.polarity == 0):
        neutral+=1
      elif(analysis.sentiment.polarity < 0):
        negative+=1
      elif(analysis.sentiment.polarity > 0):
        positive+=1
    positive=percentage(positive, SearchTerms)
    negative=percentage(negative, SearchTerms)
    neutral=percentage(neutral, SearchTerms)
    polarity=percentage(polarity, SearchTerms)

    positive=format(positive,'0.2f')
    negative=format(negative,'0.2f')
    neutral=format(neutral,'0.2f')

# Evaluating the polarity of the entered topic
    if(polarity == 0.00):
      output="Neutral"
    elif(polarity < 0.00):
      output="Negative"
    elif(polarity > 0.00):
      output="Positive"

# Returning the resultant output to the front end    
    return render_template('index.html', prediction_text='Overall Sentiment : {}'.format(output))


if __name__ == "__main__":
    app.run(debug=True)