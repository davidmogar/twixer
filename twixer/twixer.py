__version__ = '0.1.0'

import configparser
import genderator
import logging
import logging.config
import os
import sys

from flask import Flask, render_template, request
from .lib import facepp
from .scrapper import TwitterScrapper

# Setup logging
logging.config.fileConfig('twixer/config/logging.conf')
logger = logging.getLogger(__name__)

# Load configuration file
config = configparser.ConfigParser()
if not config.read('twixer/config/config.ini'):
    logger.error('Missing config file. Have you defined it?')
    sys.exit()

# Prepare Flask
app = Flask(__name__)

# Prepare genderator
guesser = genderator.Parser()

# Prepare Face++
data = config['facepp']
api = facepp.API(data['key'], data['secret'], data['server'])

# Load lexicon
lexicon = {}
with open(os.path.join(os.path.dirname(__file__), 'data/lexicon.tsv'), 'r', encoding='utf-8') as file:
    for line in file:
        word, llr = line.split('\t')
        lexicon[word.strip()] = float(llr)


def get_lexicon_classification(tweets):
    female_words, male_words = 0, 0
    female_words_list, male_words_list = [], []

    for tweet in tweets:
        if 'text' in tweet:
            for word in tweet['text'].split():
                if word in lexicon:
                    if lexicon[word] > 0:
                        female_words += 1
                        female_words_list.append(word)
                    else:
                        male_words += 1
                        male_words_list.append(word)

    if female_words != male_words:
        classification = {}
        if female_words > male_words:
            classification['gender'] = 'Female'
            classification['words'] = ', '.join(female_words_list)
        else:
            classification['gender'] = 'Male'
            classification['words'] = ', '.join(male_words_list)
        classification['confidence'] = max(female_words, male_words) / (female_words + male_words)

        return classification
    else:
        return None


def get_total_confidence(user_data):
    female, male = 0, 0
    female_conficente, male_conficente = 0, 0

    if 'genderator' in user_data:
        if user_data['genderator']['gender'] == 'Female':
            female += 1
            female_conficente += user_data['genderator']['confidence']
        else:
            male += 1
            male_conficente += user_data['genderator']['confidence']
    if 'facepp' in user_data:
        if user_data['facepp']['value'] == 'Female':
            female += 1
            female_conficente += user_data['facepp']['confidence'] / 100
        else:
            male += 1
            male_conficente += user_data['facepp']['confidence'] / 100
    if 'lexicon' in user_data:
        if user_data['lexicon']['gender'] == 'Female':
            female += 1
            female_conficente += user_data['lexicon']['confidence']
        else:
            male += 1
            male_conficente += user_data['lexicon']['confidence']
    if female != male:
        if female > male:
            user_data['gender'] = 'Female'
            user_data['confidence'] = female_conficente / (female_conficente + male_conficente)
        else:
            user_data['gender'] = 'Male'
            user_data['confidence'] = male_conficente / (female_conficente + male_conficente)

    return user_data


def get_user_data(username):
    user_data = TwitterScrapper().scrap(username)
    if user_data is not None:
        prediction = guesser.guess_gender(user_data['user_name'])
        if prediction is not None:
            user_data['genderator'] = prediction
        answer = api.detection.detect(url=user_data['profile_image'])
        if len(answer['face']) == 1:
            user_data['facepp'] = answer['face'][0]['attribute']['gender']
        prediction = get_lexicon_classification(user_data['tweets'])
        if prediction is not None:
            user_data['lexicon'] = prediction
        return get_total_confidence(user_data)
    else:
        return None


@app.route('/')
def route_index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def route_show_user_gender():
    user_data = get_user_data(request.form['username'])
    if user_data is None:
        return '404'
    else:
        return render_template('prediction.html', user_data=user_data)


def main():
    app.run()