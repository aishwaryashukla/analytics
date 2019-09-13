""""
(c)  2018 BlackRock.  All rights reserved.


To run this

Change DEV_PORT to a different number (try your phone extension!)

    venv/bin/python flask_example.py

Browse to the URL given after starting and you should see 'We are home!' - NB if running this on a PC then
change the 0.0.0.0 to localhost in the URL to use. If running from a dev box change it to the hostname

Browse to URL/security/123456789 and you should see it return the database record as JSON

"""
import os
import logging

from flask import Flask, jsonify,render_template, request, json, redirect, url_for

from flale import start_heartbeat, url_prefix_middleware
from blkcore.util import init_logging
from blkdbi.dataobject import DataObject
os.environ["defaultWebServer"] = "https://webster.bfm.com"
DEV_PORT = 233841
init_logging(level=logging.INFO)

start_heartbeat()

dbh = DataObject('DSREAD')
application = Flask(__name__)
url_prefix_middleware(application, prefix='/web/pythonapps/flask_example')


@application.route('/')
def home():
    my_home = url_for('home', _external=True)
    return render_template('arch.html', home_url=my_home)
    # return render_template("arch.html")


@application.route('/test')
def test():
    my_home = url_for('home', _external=True)
    return "Hello Aishwarya "


@application.route('/security/<cusip>')
def security_lookup(cusip):
    """Lookup a cusip in sec_master

    :param cusip: The cusip to lookup
    :return: the records as a list of dictionaries in Json format.
    """
    sql = 'SELECT * FROM {} WHERE cusip=?'.format(dbh.get_table('sec_master'))
    rows = dbh.do_sql(sql, cusip)
    if len(rows) == 0:
        result = {'status': 'Not found'}
    else:
        fields = dbh.get_result_column_names()
        result = [dict(zip(fields, r)) for r in rows]
        # timestamp is not easily convertible to json so drop it
        for r in result:
            del r['timestamp']
    return jsonify(result)


if __name__ == "__main__":
    application.secret_key = 'sec'
    # The 0.0.0.0 means accept requests on all network interfaces
    application.run(host=os.getenv('HOST', '0.0.0.0'), port=os.getenv('PORT', DEV_PORT))
