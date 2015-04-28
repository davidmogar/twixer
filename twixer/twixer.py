__version__ = '0.1.0'

import argparse
import configparser
from .facepp import API
import tweepy


def parse_arguments():
    """Define this application arguments and validate input
    :return: parsed arguments
    """
    parser = argparse.ArgumentParser(description='', prog='twixer')
    parser.add_argument('account', help='target user\'s Twitter account name')
    parser.add_argument("-v", '--verbose', help="increase output verbosity", action="store_true")

    return parser.parse_args()


def main():
    args = parse_arguments()



def foo():
    # Load Twitter keys from configuration file
    config = configparser.ConfigParser()
    config.read('twixer/config.ini')
    keys = config['twitter']

    auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
    auth.set_access_token(keys['access_token'], keys['access_token_secret'])

    api = tweepy.API(auth)

    user = api.get_user('marianorajoy')

    faceppKeys = config['facepp']
    faceppApi = API(faceppKeys['key'], faceppKeys['secret'], faceppKeys['server'])

    answer = faceppApi.detection.detect(url=user.profile_image_url)
    if answer['face']:
        print(user.screen_name + ": " + str(answer['face'][0]['attribute']['gender']))
    else:
        print("Can't determine gender")
