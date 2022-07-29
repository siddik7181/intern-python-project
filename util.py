import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError

"""
TODO: Write whatever class or function you may need
but, don't use any third party library
feel free to make any changes in the given class and its methods' arguments or implementation as you see fit
"""


class NetworkRequest:
    @staticmethod
    def get(url, headers = {}):
        req = Request(url=url, method='GET')
        for key, value in headers.items():
            req.add_header(key, value)
        
        result = {}
        with urlopen(req) as res:
            body = res.read().decode('utf-8')
            result['body'] = json.loads(body)
            result['code'] = res.status
        
        return result
    
    @staticmethod
    def post():
        pass

    @staticmethod
    def put():
        pass

    @staticmethod
    def delete():
        pass

