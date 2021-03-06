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
    female_confidence, male_confidence = 0, 0
    classifications = 0
    words_list = {}

    for tweet in tweets:
        if 'text' in tweet:
            female_words, male_words = 0, 0
            for word in tweet['text'].split():
                if word in lexicon and word not in words_list:
                    if lexicon[word] > 0:
                        female_words += 1
                    else:
                        male_words += 1
                    words_list[word] = lexicon[word]

            if female_words != male_words:
                classifications += 1
                if female_words > male_words:
                    female_confidence += female_words / (female_words + male_words)
                else:
                    male_confidence += male_words / (female_words + male_words)

    classification = {}
    female_confidence /= classifications or 1
    male_confidence /= classifications or 1
    if female_confidence != male_confidence:
        if female_confidence > male_confidence:
            classification['gender'] = 'Female'
        else:
            classification['gender'] = 'Male'
        classification['words'] = words_list
        classification['confidence'] = max(female_confidence, male_confidence)
        return classification
    else:
        return None


def get_total_confidence(user_data):
    female, male = 0, 0
    female_confidence, male_confidence = 0, 0
    analysis = 0

    if 'genderator' in user_data:
        analysis += 1
        if user_data['genderator']['gender'] == 'Female':
            female += 1
            female_confidence += user_data['genderator']['confidence']
        else:
            male += 1
            male_confidence += user_data['genderator']['confidence']
    if 'facepp' in user_data:
        analysis += 1
        if user_data['facepp']['value'] == 'Female':
            female += 1
            female_confidence += user_data['facepp']['confidence'] / 100
        else:
            male += 1
            male_confidence += user_data['facepp']['confidence'] / 100
    if 'lexicon' in user_data:
        analysis += 1
        if user_data['lexicon']['gender'] == 'Female':
            female += 1
            female_confidence += user_data['lexicon']['confidence']
        else:
            male += 1
            male_confidence += user_data['lexicon']['confidence']
    if female != male:
        if female > male:
            user_data['gender'] = 'Female'
            user_data['confidence'] = (female_confidence + (1 - (male_confidence or 1))) / analysis
        else:
            user_data['gender'] = 'Male'
            user_data['confidence'] = (male_confidence + (1 - (female_confidence or 1))) / analysis

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
        return render_template('index.html', error=True)
    else:
        return render_template('prediction.html', user_data=user_data)


def main():
    app.run(host='0.0.0.0')