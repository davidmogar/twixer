import logging
import urllib.request

from bs4 import BeautifulSoup

TWITTER_BASE_URL = 'https://twitter.com/'


class TwitterScrapper():

    _logger = logging.getLogger(__name__)

    def scrap(self, username):
        """
        Performs a scrap over the given Twitter user profile page to get some info about him/her and
        returns this data in a dictionary.

        Params:
            username (string): Username of the user scrap.

        Returns:
            A dictionary with all scrapped data.
        """
        user_data = {}

        try:
            with urllib.request.urlopen(TWITTER_BASE_URL + username) as response:
                soup = BeautifulSoup(response.read())
                user_data['profile_image'] = self._get_profile_image_url(soup)
                user_data['user_name'] = self._get_user_name(soup)
                user_data['tweets'] = self._get_user_tweets(soup)
        except urllib.error.HTTPError as e:
            self._logger.error('The server couldn\'t fulfill the request. Error code ' + str(e.code))

        return user_data or None

    def _get_profile_image_url(self, soup):
        """
        Returns the user's profile image url as found in the html response but removing _400x400 to get
        a bigger image.

        Params:
            soup (BeautifulSoup): BeautifulSoup object with parsed response.

        Returns:
            The profile image of the user requested or None if not found.
        """
        image = soup.find('img', {'class': 'ProfileAvatar-image'})
        if image is not None:
            return image['src'].replace('_400x400', '')
        return None

    def _get_user_tweets(self, soup, include_retweets=False):
        """
        Returns a list with all the tweets found in the html response. Each element of the list is a dictionary
        with information about the author and the text.

        Params:
            soup (BeautifulSoup): BeautifulSoup object with parsed response.

        Returns:
            A list of tweets in the timeline of the user requested.
        """
        tweets = []
        tweet_nodes = soup.find_all('div', {'class': 'ProfileTweet'})

        for tweet_node in tweet_nodes:
            if include_retweets or tweet_node.get('data-retweet-id') is None:
                tweets.append({
                    'author_fullname': tweet_node.find('b', {'class': 'ProfileTweet-fullname'}).text.strip(),
                    'author_screenname': tweet_node.find('span', {'class': 'ProfileTweet-screenname'}).text.
                            replace('<span class="at">@</span>', '').strip(),
                    'text': tweet_node.find('p', {'class': 'ProfileTweet-text'}).text.strip()
                })

        return tweets

    def _get_user_name(self, soup):
        """
        Returns the user name as found in the html response.

        Params:
            soup (BeautifulSoup): BeautifulSoup object with parsed response.

        Returns:
            The name of the user requested or None if not found.
        """
        username = soup.find('a', {'class': 'ProfileHeaderCard-nameLink'})
        if username is not None:
            return username.text
        return None