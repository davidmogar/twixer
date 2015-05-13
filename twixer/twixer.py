__version__ = '0.1.0'

import configparser
import logging
import logging.config
import sys

from flask import Flask, render_template

# Setup logging
logging.config.fileConfig('twixer/config/logging.conf')
logger = logging.getLogger(__name__)

# Load configuration file
config = configparser.ConfigParser()
if not config.read('twixer/config/config.ini'):
    sys.exit()

# Prepare Flask
app = Flask(__name__)


@app.route('/')
def route_index():
    return render_template('index.html')

@app.route('/<username>')
def show_user_gender(username):
    return '%s is a robot' % username


def main():
    app.run()