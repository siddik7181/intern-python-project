from time import time
from util import NetworkRequest

def time_decorator(func):
    def inner(*args, **kwargs):
        start = time()
        res = func(*args, **kwargs)
        end = time()
        print(f"(time taken: {end - start} ms)")
        return res
    return inner

def rotate_token(func):
    def inner(self, *args, **kwargs):
        res = func(self, *args, **kwargs)
        if res['code'] != 401:
            return res
        
        print('Refreshing Token!!')
        refresh_token_res = NetworkRequest.post('/auth/token', {
                'refresh_token': self.refresh_token
        })

        if refresh_token_res['code'] == 200:
            self.save_tokens(refresh_token_res['body'])
            res = func(self, *args, **kwargs)
            return res
        
        print(f'Error orrcured: {refresh_token_res}')
        return res
    return inner