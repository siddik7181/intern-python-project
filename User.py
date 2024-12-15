
from util import NetworkRequest
from decorators import time_decorator, rotate_token

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
        filename='nahid.log', 
        filemode='w', 
        level=logging.DEBUG, 
        format='%(levelname)s %(asctime)s %(name)s: %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p')

class User:

    def __init__(self):
        self.access_token = None
        self.refresh_token = None
        self.token_type = None

    def login(self, username, password):
        print('Loggin in...')
        logger.debug('Loggin in...')

        user = NetworkRequest.post('/auth', {
                "username": username, 
                "password": password
            })
        if user['code'] != 200 or 'body' not in user:
            print('Please Register Yourself!')
            logger.debug('Please Register Yourself!')

            firstname = input('Firstname: ')
            lastname = input('Lastname: ') 
            self.register(username, firstname, lastname, password)
        else:
            self.tokens = self.save_tokens(user['body'])
            print('Log in successfull')
            logger.debug('Log in successfull')

    def register(self, username, firstname, lastname, password):
        print('New user registering ...')
        logger.debug('New user registering ...')

        user = NetworkRequest.post('/users', { 
                "username": username,
                "firstname": firstname,
                "lastname": lastname,
                "password": password
            })
        if user['code'] != 200:
            print(f"Error: {user['message']}")
            logger.warning('Error Occured: %s', user['message'])

        else:
            print('Registration done ...')
            logger.debug('Registration done ...')

            self.login(username, password)

    def save_tokens(self, body):
        self.access_token = body.get('access_token')
        self.refresh_token = body.get('refresh_token')
        self.token_type = body.get('token_type')
    
    def show_tweets(self):
        for tweet in self.recent_tweets:
            print(f"({tweet['id']}) {tweet['author']['username']} tweeted at {tweet['created_at']}")
            logger.debug('(%s) %s tweeted at %s', tweet['id'], tweet['author']['username'], tweet['created_at'])
            print(tweet['text'] + "\n")
            logger.info('%s', tweet['text'])
            logger.info('')

 
    @time_decorator
    @rotate_token
    def get_tweets(self):
        print('checking recent tweets ...')
        logger.debug('checking recent tweets ...')
        tweets = NetworkRequest.get('/tweets?skip=0&limit=5',headers={
            'Authorization': 'Bearer ' + self.access_token
        })
        
        self.recent_tweets = tweets.get('body')
        return tweets

    
    @time_decorator
    @rotate_token
    def post_tweets(self, tweet):
        print('posting tweet ...')
        logger.debug('posting tweet ...')
        posted_tweet = NetworkRequest.post('/tweets', body={ "text": tweet }, headers={
                    'Authorization': 'Bearer ' + self.access_token
                })
        
        print(tweet)
        logger.debug('%s', tweet)
        return posted_tweet