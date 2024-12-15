from getpass import getpass
from User import User
from pyjokes import get_joke
from time import sleep
import json
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
        filename='nahid.log', 
        filemode='w', 
        level=logging.DEBUG, 
        format='%(levelname)s %(asctime)s %(name)s: %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p')

def main():

    print('Please login to your account')
    logger.info('Please login to your account')

    username = input('Username: ')
    password = getpass('Password: ')
    all_tweets = set()

    logger.info('Username: %s', username)
    logger.info('Password: ')

    user = User()
    user.login(username, password)

    tweets = (user.get_tweets()).get('body')
    user.show_tweets()

    for tweet in tweets:
        all_tweets.add(json.dumps(tweet))

    new_tweets = 0
    while new_tweets < 10:
        tweet = get_joke()
        if tweet not in all_tweets:
            posted_tweet = (user.post_tweets(tweet)).get('body')
            if isinstance(posted_tweet, dict):
                all_tweets.add(json.dumps(posted_tweet))
                new_tweets += 1
                
                if new_tweets < 10:
                    print('posted tweet. sleeping 1 min now.')
                    logger.debug('posted tweet. sleeping 1 min now.')
                else:
                    print('posted tweet.')
                    logger.debug('posted tweet.')
            else:
                print("couldn't posted sorry, sleeping 1 min now ...")
                logger.error("couldn't posted sorry, sleeping 1 min now ...")
            sleep(1)
    
    print('10 new tweets posted ...')
    logger.info('10 new tweets posted ...')


if __name__ == '__main__':
    main()
