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

from flask import Flask, jsonify
from flale import start_heartbeat, url_prefix_middleware
from blkcore.util import init_logging
from blkdbi.dataobject import DataObject
from beam2py import send_beam2, Beam2Payload, bms_source
from blkbms.bms import BMS

DEV_PORT = 233841
init_logging(level=logging.INFO)
source_id = bms_source('ASSETINFO_LITE')
bmso = BMS(appname='flask_example_bms')

start_heartbeat()

dbh = DataObject('DSREAD')
application = Flask(__name__)
url_prefix_middleware(application, prefix='/web/pythonapps/flask_example_bms')


@application.route('/')
def home():
    return 'We are home!'


@application.route('/security/<cusip>')
def security_lookup(cusip):
    """get identifiers for a cusip via AssetInfoServer

    :param cusip: The cusip to lookup
    :return: the records as a list of dictionaries in Json format.
    """
    payload = Beam2Payload('IDENTIFIERS', {'cusips': [cusip]})
    resp = send_beam2(bmso, source_id, payload, 30)
    return jsonify([r.output for r in resp])


if __name__ == "__main__":
    application.secret_key = 'sec'
    # The 0.0.0.0 means accept requests on all network interfaces
    application.run(host=os.getenv('HOST', '0.0.0.0'), port=os.getenv('PORT', DEV_PORT))
