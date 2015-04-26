import configparser
import facepp
import tweepy

# Load Twitter keys from configuration file
config = configparser.ConfigParser()
config.read('config.ini')
keys = config['twitter']

auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
auth.set_access_token(keys['access_token'], keys['access_token_secret'])

api = tweepy.API(auth)

user = api.get_user('marianorajoy')

faceppKeys = config['facepp']
faceppApi = facepp.API(faceppKeys['key'], faceppKeys['secret'], faceppKeys['server'])

answer = faceppApi.detection.detect(url=user.profile_image_url)
if answer['face']:
    print(user.screen_name + ": " + str(answer['face'][0]['attribute']['gender']))
else:
    print("Can't determine gender")
