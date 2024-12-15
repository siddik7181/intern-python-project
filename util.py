import json
from urllib.request import Request, urlopen

"""
TODO: Write whatever class or function you may need
but, don't use any third party library
feel free to make any changes in the given class and its methods' arguments or implementation as you see fit
"""


class NetworkRequest:
    base_url = 'http://127.0.0.1:8000/api'
    @staticmethod
    def call_api(method, url, body = {}, headers = {}):
        result = {}
        try:
            full_url = NetworkRequest.base_url + url
            data = json.dumps(body).encode('utf-8')
            req = Request(url= full_url, data=data, method=method)

            req.add_header('Content-Type', 'application/json')
            for key, value in headers.items():
                req.add_header(key, value)

            with urlopen(req) as res:
                body = res.read().decode('utf-8')
                result['body'] = json.loads(body)
                result['code'] = res.status

        except Exception as e:
            result['code'] = e.status
            result['message'] = str(e)
        
        finally:
            return result

    @staticmethod
    def get(url, headers={}):
        return NetworkRequest.call_api(method='GET', url=url, headers=headers)
    
    @staticmethod
    def post(url, body={}, headers={}):
        return NetworkRequest.call_api(method='POST', url=url, body=body, headers=headers)
        
    @staticmethod
    def put(url, body={}, headers={}):
        return NetworkRequest.call_api(method='PUT', url=url, body=body, headers=headers)

    @staticmethod
    def delete(url, body={}, headers={}):
        return NetworkRequest.call_api(method='DELETE', url=url, body=body, headers=headers)

