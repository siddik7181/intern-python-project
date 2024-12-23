from database import createdb, addData
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

    logger.info('Username: %s', username)
    logger.info('Password: ')

    user = User()
    user.login(username, password)

    tweets = (user.get_tweets()).get('body')
    user.show_tweets()

    with createdb() as cursor: 
        for tweet in tweets:
            print(f"Tweet Text: {tweet['text']}")
            logger.debug(tweet['text'])
            try:
                addData(cursor, table="tweets", column="tweet", column_value=tweet['text'])
            except ValueError as e:
                print(e)
                logger.error(e)

    new_tweets = 0
    while new_tweets < 10:
        tweet = get_joke()
        with createdb() as cursor: 
            try:
                addData(cursor, table="tweets", column="tweet", column_value=tweet)
                posted_tweet = (user.post_tweets(tweet)).get('body')
                new_tweets += 1
                if new_tweets < 10:
                    print('posted tweet. sleeping 1 min now.')
                    logger.debug('posted tweet. sleeping 1 min now.')
                else:
                    print('posted tweet.')
                    logger.debug('posted tweet.')
                sleep(1)

            except ValueError as e:
                print(e)
                logger.error(e)

    print('10 new tweets posted ...')
    logger.info('10 new tweets posted ...')


if __name__ == '__main__':
    main()
