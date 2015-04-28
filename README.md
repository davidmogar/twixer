
# twixer
[![Build Status](https://travis-ci.org/davidmogar/twixer.svg?branch=master)](https://travis-ci.org/davidmogar/twixer)

Twixer is a simple tool to identify a Twitter user gender given his/her username. To achieve this, twixer analizes last tweets and bio information and apply facial recognition over the user profile image using an external service.

## Configuration
Prior to execute the application it is needed to define a configuration file with Twitter and Facepp credentials. I'll change this at some moment but by now you need a file like this one:
```
[twitter]
consumer_key=
consumer_secret=
access_token=
access_token_secret=

[facepp]
key=
secret=
server=http://api.us.faceplusplus.com/
```

To make it a little easier, there is a sample file inside config folder. Just rename it to ```config.ini``` and fill the gaps.

## Usage
The tool is user friendly. You only have to set the username of the user you want to analyze and let twixer do its job. Need more info? This could help you:
```
usage: python -m twixer [-h] [-v] username

positional arguments:
  username       target Twitter username

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  increase output verbosity
```

## To-do
At the moment I'm only applying facial recognition so there is still a loooooot of things to be done. I'll update this section when the code to be written is less than the items on To-do list.

## Questions that no one ever asks
1. **Why Twixer?**

   I spent a day thinking in a good name but I could only think in [chick sexing](http://en.wikipedia.org/wiki/Chick_sexing) so I ended up calling this app twitter-sexer. That name was too long so I renamed it to twixer.
2. **Is facial recognition useful to find out a Twitter user gender?**

   Yes and no. It's a nice approach but [Face++](http://faceplusplus.com), the service used to apply facial recognition, is not reliable. This is a point to be improved in future versions.
3. **Any plans to upload this app to PyPi?**

   Yep, I'll upload it but I need to implement a lot of things yet, and this is gonna take some time.
