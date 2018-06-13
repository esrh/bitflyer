import os
import json
import requests
import time
import hmac
import hashlib
import sys,time
 

class ApiCall:
    def __init__(self,api_key,api_secret,api_endpoint):
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_endpoint = api_endpoint
        
    def get_api_call(self,path):
        method = 'GET'
        timestamp = str(time.time())
        text = timestamp + method + path
        sign = hmac.new(bytes(self.api_secret.encode('ascii')), bytes(text.encode('ascii')), hashlib.sha256).hexdigest()
        request_data=requests.get(
            self.api_endpoint+path
            ,headers = {
                'ACCESS-KEY': self.api_key,
                'ACCESS-TIMESTAMP': timestamp,
                'ACCESS-SIGN': sign,
                'Content-Type': 'application/json'
            })
        return request_data
    
    
    def post_api_call(self,path,body):
        body = json.dumps(body)
        method = 'POST'
        timestamp = str(time.time())
        text = timestamp + method + path + body
        sign = hmac.new(bytes(self.api_secret.encode('ascii')), bytes(text.encode('ascii')), hashlib.sha256).hexdigest()
        request_data=requests.post(
            self.api_endpoint+path
            ,data= body
            ,headers = {
                'ACCESS-KEY': self.api_key,
                'ACCESS-TIMESTAMP': timestamp,
                'ACCESS-SIGN': sign,
                'Content-Type': 'application/json'
            })
        return request_data
        


class bitapi:
    def __init__(self):
        with open(os.path.expanduser('~/important/token/bitflyer.txt'), 'r') as f:
            api_key, api_secret = f.read().split('\n')
        api_endpoint = 'https://api.bitflyer.jp'
        self.api = api_key, api_secret, api_endpoint

    def itainfo(self, count):
        count2 = 100
        api = ApiCall(self.api[0], self.api[1], self.api[2])
        path = '/v1/getboard?product_code=BTC_JPY'
        BTCJPY = api.get_api_call(path).json()["mid_price"]
        path = '/v1/getboard?product_code=FX_BTC_JPY'
        result = api.get_api_call(path).json()   
        t_uri = 0
        all_uri = []
        mid_price = result["mid_price"]
        for i,uri in enumerate(result["bids"]):
            all_uri.append(uri["price"])
            t_uri = t_uri + uri["price"]
            if i > 10:
                break
        a_uri = t_uri / count
        a_uri = sum(all_uri)/len(all_uri)/count2
        a_uri = int(a_uri)
        t_kai = 0
        all_kai = []
        for i,kai in enumerate(result["asks"]):
            all_kai.append(kai["price"])
            t_kai = t_kai + kai["price"]
            if i > 10:
                break
        a_kai = t_kai / count
        a_kai = sum(all_kai)/len(all_kai)/count2
        a_kai = int (a_kai)
        return a_uri,a_kai,mid_price,BTCJPY
        
    def nariyuki(self, baibai, ryou):
        path = '/v1/me/sendchildorder'
        api = ApiCall(self.api[0], self.api[1], self.api[2])
        body = {
            "product_code": "FX_BTC_JPY",
            "child_order_type": "MARKET",
            "side": baibai,
            "size": ryou,
            "minute_to_expire": 10000,
            "time_in_force": "GTC"
        }
        result = api.post_api_call(path,body).json()
        print(result)
    
    
if __name__ == '__main__':
    coin = bitapi()
    for x in range(1,1000):
        p = coin.itainfo(10)
        print(p)
        time.sleep(3)
