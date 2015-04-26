import configparser
import tweepy

# Load Twitter keys from configuration file
config = configparser.ConfigParser()
config.read('config.ini')
keys = config['twitter']

auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
auth.set_access_token(keys['access_token'], keys['access_token_secret'])

api = tweepy.API(auth)

user = api.get_user('davidmogar')

print(user.screen_name)
print(user.followers_count)

for friend in user.friends():
    print(friend.screen_name)