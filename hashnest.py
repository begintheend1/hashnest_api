from urllib import urlencode
import urllib2,json
import time,datetime
import hashlib,hmac,base64


#SELL='sale'
#BUY='purchase'
class hashnest(object):
    
    URL = 'https://www.hashnest.com/api/v1/'
 
    def __init__(self,username,key,secret):
        self.username=username
        self.key=key
        self.secret=secret
 

    def get_nonce(self):
        self.utcnow=a=datetime.datetime.utcnow()
        b=datetime.datetime(1970,1,1,0,0,0,0)
        self.nonce= int((a-b).total_seconds()*1000)
        return self.nonce

    def signature(self,req):
        nonce=self.get_nonce()
        message = str(nonce) + self.username + self.key
        req['access_key']=self.key
        req['nonce']=nonce
        req['signature']= hmac.new(self.secret, msg=message, digestmod=hashlib.sha256).hexdigest() 
        return urlencode(req)
     
    def request(self,url,req={}):
        url = self.URL + url
        data= self.signature(req)
        info = urllib2.Request(url, data)
        resp = urllib2.urlopen(info)
        r=resp.read()
        return r
  
    
    def get_account_info(self):
        return self.request('account')
  
    def get_account_balance(self):
        return self.request('currency_accounts')
  
    def get_account_hashrate(self):
        return self.request('hash_accounts')
  
    def get_orders(self,cmi):
        param={'currency_market_id':cmi}
        return self.request('orders/active',param)
  
    def get_history(self,cmi,page=1,page_amount=10):
        param={'currency_market_id':cmi}
        param['page']=page
        param['page_per_amount']=page_amount
        return self.request('orders/history',param)
  
    def create_order(self,cmi,amount,ppc,category):
        param={'currency_market_id':cmi}
        param['amount']=amount
        param['ppc']=ppc
        param['category']=category
        return self.request('orders',param)
  
    def delete_order(self,order_id):
        param={'order_id':order_id}
        return self.request('orders/revoke',param)
  
    def delete_all_orders(self,cmi,category):
        param={'currency_market_id':cmi}
        param['category']=category
        return self.request('orders/quick_revoke',param)
  
    def get_opened_markets(self):
        return self.request('currency_markets')
  
    def get_currency_orders(self,cmi):
        param={'currency_market_id':cmi}
        return self.request('currency_markets/orders',param)
  
    def get_currency_trades(self,cmi,category,page=1,page_amount=10):
        param={'currency_market_id':cmi}
        param['page']=page
        param['page_per_amount']=page_amount
        param['category']=category
        return self.request('currency_markets/order_history',param)
  

  
