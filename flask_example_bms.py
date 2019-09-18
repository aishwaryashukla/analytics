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

from flask import Flask,render_template,request,json,redirect,url_for
import csv

import numpy as np
from datetime import datetime
import pytz
from pytz import timezone


DEV_PORT = 233841
application = Flask(__name__)
application.secret_key = 'sec'

@application.route('/')

def root():
    my_home = url_for('home', _external=True)
    return render_template('index.html', home_url = my_home)


@application.route('/homecontact')

def homecontact():
    my_home = url_for('home', _external=True)
    return render_template('tech-contact.html', home_url = my_home)


@application.route('/homepage1')

def page1():
    my_home = url_for('home', _external=True)
    return render_template('tech-category-01.html', home_url = my_home)

@application.route('/homepage2')

def page2():
    my_home = url_for('home', _external=True)
    return render_template('tech-category-02.html', home_url = my_home)

@application.route('/homepage3')

def page3():
    my_home = url_for('home', _external=True)
    return render_template('tech-category-03.html', home_url = my_home)

@application.route('/home')

def home():
    my_home = url_for('home', _external=True)

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


if __name__ == "__main__":
    application.secret_key = 'sec'
    # The 0.0.0.0 means accept requests on all network interfaces
    application.run(host=os.getenv('HOST', 'localhost'), port=os.getenv('PORT', DEV_PORT))
