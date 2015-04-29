__version__ = '0.1.0'

import argparse
import configparser
import logging
import logging.config
import sys
import tweepy

from .lib import facepp

# Setup logging
logging.config.fileConfig('twixer/config/logging.conf')
logger = logging.getLogger(__name__)

# Load configuration file
config = configparser.ConfigParser()
if not config.read('twixer/config/config.ini'):
    logger.error('Missing config file. Have you defined it?')
    sys.exit()


def get_user_object(username):
    """
    Returns an object with information about the specified user.

    Parameters:
        username: Username of the target user.

    Returns:
        An object with the user information.
    """
    logger.debug('Getting user information')

    oauth = config['twitter']

    auth = tweepy.OAuthHandler(oauth['consumer_key'], oauth['consumer_secret'])
    auth.set_access_token(oauth['access_token'], oauth['access_token_secret'])
    api = tweepy.API(auth)

    return api.get_user(username)


def parse_arguments():
    """
    Define this application arguments and validate input

    Returns:
        Parsed arguments.
    """
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('username', help='target Twitter username')
    parser.add_argument("-v", '--verbose', help="increase output verbosity", action="store_true")

    return parser.parse_args()


def main():
    args = parse_arguments()
    if args.verbose:
        global logger
        logger.setLevel(logging.DEBUG)

    user = get_user_object(args.username)

    # Apply facial recognition
    logger.debug('Applying facial recognition')

    data = config['facepp']
    api = facepp.API(data['key'], data['secret'], data['server'])

    answer = api.detection.detect(url=user.profile_image_url.replace('_normal', ''))
    if len(answer['face']) == 1:
        logger.info(user.screen_name + ": " + str(answer['face'][0]['attribute']['gender']))
    else:
        logger.warning("Can't determine gender")
