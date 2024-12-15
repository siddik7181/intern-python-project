from getpass import getpass
from User import User
from pyjokes import get_joke
from time import sleep
from util import NetworkRequest
import json

def main():

    print('Please login to your account')
    username = input('Username: ')
    password = getpass('Password: ')
    all_tweets = set()

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
                print('posted tweet. ', end='')
                if new_tweets < 10:
                    print('sleeping 1 min now.')
            else:
                print("couldn't posted sorry, sleeping 1 min now ...")
            sleep(1)
    
    print('10 new tweets posted ...')


if __name__ == '__main__':
    main()
