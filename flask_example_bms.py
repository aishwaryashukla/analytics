""""
(c)  2018 BlackRock.  All rights reserved.


To run this

Change DEV_PORT to a different number (try your phone extension!)

    venv/bin/python flask_example.py

Browse to the URL given after starting and you should see 'We are home!' - NB if running this on a PC then
change the 0.0.0.0 to localhost in the URL to use. If running from a dev box change it to the hostname

Browse to URL/security/123456789 and you should see it return the database record as JSON

"""
from flask import Flask,render_template,json,redirect,url_for,session, escape, request

import os
import logging
import pandas as pd
import datetime
from flask import Flask, jsonify
from datetime import datetime
import sys
import got3 as got
import pprint

from flask import Flask,render_template,request,json,redirect,url_for
import csv

import numpy as np
from datetime import datetime
import pytz
# import sentiment
from pytz import timezone

import nltk

nltk.download('vader_lexicon')
nltk.download('punkt')

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import sentiment
from nltk import word_tokenize


sid = SentimentIntensityAnalyzer()
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')


DEV_PORT = 233841
application = Flask(__name__)
application.secret_key = 'sec'

@application.route('/')

def root():
    my_home = url_for('root', _external=True)
    print(my_home)
    return render_template('index.html', home_url = my_home)


@application.route('/contact')

def contact():
    my_home = url_for('root', _external=True)
    return render_template('tech-contact.html', home_url = my_home)


@application.route('/page1')

def page1():
    my_home = url_for('root', _external=True)
    return render_template('tech-category-01.html', home_url = my_home)

@application.route('/page2')

def page2():
    my_home = url_for('root', _external=True)
    return render_template('tech-category-02.html', home_url = my_home)

@application.route('/page3')

def page3():
    my_home = url_for('root', _external=True)
    return render_template('tech-category-03.html', home_url = my_home)

@application.route('/test', methods=['GET', 'POST'])
def test():
    # Example 1 - Get tweets by username
    tsearch = request.args.get('entry2_id')
    print(request.args.get('entry1_id'))


    # tweetCriteria = got.manager.TweetCriteria().setUsername('arvindkejriwal').setMaxTweets(4)
    # tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]
    # pprint.pprint(tweet)
    # print(type(tweet))
    # printTweet("### Example 1 - Get tweets by username [arvindkejriwal]", tweet)

    # Example 2 - Get tweets by query search
    tweetCriteria = got.manager.TweetCriteria().setQuerySearch(tsearch).setSince("2019-01-01").setUntil(
        "2019-10-01").setMaxTweets(10)
    tweets= got.manager.TweetManager.getTweets(tweetCriteria)
    total_compound = 0
    total_score ={'neg': 0.0, 'neu': 0.0, 'pos': 0.0, 'compound': 0.0}
    for tweet in tweets:

        scores = sid.polarity_scores(tweet.text)
        total_score['neg'] += scores['neg']
        total_score['neu'] += scores['neu']
        total_score['pos'] += scores['pos']
        total_score['compound'] += scores['compound']

        total_compound = total_compound + scores['compound']
        print("tsearch = {} \n tweet = {} \n score = {}".format(tsearch, tweet.text, scores))
        # printTweet("### Get tweets by query search " + tsearch, tweet)
    #
    # # Example 3 - Get tweets by username and bound dates
    # tweetCriteria = got.manager.TweetCriteria().setUsername("barackobama").setSince("2015-09-10").setUntil(
    #     "2015-09-12").setMaxTweets(1)
    # tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]
    #
    # printTweet("### Example 3 - Get tweets by username and bound dates [barackobama, '2015-09-10', '2015-09-12']",
    #            tweet)
    # print(type(tweet))

    # return tweet.text
    return "Sentiment Analysis: "+str(total_score)
@application.route('/home')

def home():
    my_home = url_for('root', _external=True)

    '''
    this can go inside a function
    '''

    utcmoment_naive = datetime.utcnow()
    utcmoment = utcmoment_naive.replace(tzinfo=pytz.utc)
    localFormat = "%Y-%m-%d %H:%M:%S"

    timezones = ['America/Los_Angeles', 'Europe/Madrid', 'America/Puerto_Rico']
    lon = str(utcmoment.astimezone(pytz.timezone('Europe/London')).hour) + \
          ":" + str(utcmoment.astimezone(pytz.timezone('Europe/London')).minute)

    india = str(utcmoment.astimezone(pytz.timezone('Asia/Kolkata')).hour) + \
          ":" + str(utcmoment.astimezone(pytz.timezone('Asia/Kolkata')).minute)

    nyc = str(utcmoment.astimezone(pytz.timezone('America/New_York')).hour) + \
         ":" + str(utcmoment.astimezone(pytz.timezone('America/New_York')).minute)

    hk = str(utcmoment.astimezone(pytz.timezone('Hongkong')).hour) + \
          ":" + str(utcmoment.astimezone(pytz.timezone('Hongkong')).minute)

    syd = str(utcmoment.astimezone(pytz.timezone('Australia/Sydney')).hour) + \
          ":" + str(utcmoment.astimezone(pytz.timezone('Australia/Sydney')).minute)

    print(india)
    return render_template('arch.html',home_url = my_home, london = lon, india = india, nyc = nyc, syd = syd, hk = hk)



@application.route('/security/<cusip>')
def security_lookup(cusip):
    """get identifiers for a cusip via AssetInfoServer

    :param cusip: The cusip to lookup
    :return: the records as a list of dictionaries in Json format.
    """

    return "Security lookup "


def printTweet(descr, t):
    print(descr)
    print("Username: %s" % t.username)
    print("Retweets: %d" % t.retweets)
    print("Text: %s" % t.text)
    print("Mentions: %s" % t.mentions)
    print("Hashtags: %s\n" % t.hashtags)
    print("geo: %s\n" % t.geo)




if __name__ == "__main__":
    application.secret_key = 'sec'
    # The 0.0.0.0 means accept requests on all network interfaces
    application.run(host=os.getenv('HOST', 'localhost'), port=os.getenv('PORT', DEV_PORT))
