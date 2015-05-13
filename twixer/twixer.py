__version__ = '0.1.0'

import configparser
import sys

from flask import Flask

# Load configuration file
config = configparser.ConfigParser()
if not config.read('twixer/config/config.ini'):
    logger.error('Missing config file. Have you defined it?')
    sys.exit()

# Prepare Flask
app = Flask(__name__)


@app.route('/')
def route_index():
    return 'Hello World'


def main():
    app.run()