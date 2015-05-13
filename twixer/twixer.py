__version__ = '0.1.0'

import argparse
import configparser
import logging
import logging.config
import sys

from .lib import facepp

# Setup logging
logging.config.fileConfig('twixer/config/logging.conf')
logger = logging.getLogger(__name__)

# Load configuration file
config = configparser.ConfigParser()
if not config.read('twixer/config/config.ini'):
    logger.error('Missing config file. Have you defined it?')
    sys.exit()


def parse_arguments():
    """
    Define this application arguments and validate input

    Returns:
        Parsed arguments.
    """
    parser = argparse.ArgumentParser(description='')
    parser.add_argument("-v", '--verbose', help="increase output verbosity", action="store_true")

    return parser.parse_args()


def main():
    args = parse_arguments()

    if args.verbose:
        global logger
        logger.setLevel(logging.DEBUG)