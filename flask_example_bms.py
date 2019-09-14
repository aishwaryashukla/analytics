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

from flask import Flask,render_template,request,json,redirect,url_for
import csv
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker

import numpy as np



application = Flask(__name__)
application.secret_key = 'sec'
@application.route('/')

def home():
    my_home = url_for('home', _external=True)
    return render_template('arch.html',home_url = my_home)



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
    application.run(host=os.getenv('HOST', 'localhost'))
