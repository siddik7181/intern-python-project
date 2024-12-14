
from util import NetworkRequest

class User:

    def login(self, username, password):
        print('Loggin in...')
        user = NetworkRequest.post('/auth', {
                "username": username, 
                "password": password
            })
        if user['code'] != 200:
            print('Please Register Yourself!')
            firstname = input('Firstname: ')
            lastname = input('Lirstname: ') 
            self.register(username, firstname, lastname, password)
        else:
            self.access_token = user['body']['access_token'] if 'access_token' in user['body'] else None
            self.refresh_token = user['body']['refresh_token'] if 'refresh_token' in user['body'] else None
            self.token_type = user['body']['token_type'] if 'token_type' in user['body'] else None
            print('Log in successfull')

    def register(self, username, firstname, lastname, password):
        user = NetworkRequest.post('/users', { 
                "username": username,
                "firstname": firstname,
                "lastname": lastname,
                "password": password
            })
        if user['code'] != 200:
            print(f"Error: {user['message']}")
        else:
            self.login(username, password)


    def get_new_tokens(self):
        pass

    def post_tweets(self, tweet):
        pass

    def get_tweets(self, limit=5):
        pass
        