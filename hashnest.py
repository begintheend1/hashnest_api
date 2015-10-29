
from urllib import urlencode
import urllib2,json
import time,datetime
import hashlib,hmac,base64



class hashnest(object):

    BASEURL='https://www.hashnest.com/api/'
    APIVERSION='v1'
    URL=BASEURL+APIVERSION+'/'
    URL_ACCOUNT='account'
    URL_BALANCE='currency_accounts'
    URL_HASHRATE='hash_accounts'
    URL_CREATE_ORDER='orders'
    URL_ORDERS='orders/active'
    URL_HISTORY='orders/history'
    URL_DELETE_ORDER='orders/revoke'
    URL_DELETE_ALL_ORDERS='orders/quick_revoke'
    URL_OPENED_MARKETS='currency_markets'
    URL_CURRENCY_ORDERS='currency_markets/orders'
    URL_CURRENCY_TRADES='currency_markets/order_history'
    SELL='sale'
    BUY='purchase'
 


 

    def __init__(self,username,key,secret):
        self.username=username
        self.key=key
        self.secret=secret
 

    def get_nonce(self):
        self.utcnow=a=datetime.datetime.utcnow()
        b=datetime.datetime(1970,1,1,0,0,0,0)
        self.nonce= int((a-b).total_seconds()*1000)
        return self.nonce


  
  
    def sign(self,req):
        nonce=self.get_nonce()
        message = str(nonce) + self.username + self.key
        req['access_key']=self.key
        req['nonce']=nonce
        req['signature']= hmac.new( self.secret, msg=message, digestmod=hashlib.sha256).hexdigest() 
        return urlencode(req)
     
    def perform_private(self,url,req={}):
        url=baseurl=self.URL+url
        data=self.sign(req)
        request= urllib2.Request(url, data)
        resp = urllib2.urlopen(request)
        r=resp.read()
        try: return json.loads(r)
        except: return r
  
    
    def get_account_info(self):
        return self.perform_private(self.URL_ACCOUNT)
  
    def get_account_balance(self):
        return self.perform_private(self.URL_BALANCE)
  
    def get_account_hashrate(self):
        return self.perform_private(self.URL_HASHRATE)
  
    def get_orders(self,cmi):
        param={'currency_market_id':cmi}
        return self.perform_private(self.URL_ORDERS,param)
  
    def get_history(self,cmi,page=1,page_amount=20):
        param={'currency_market_id':cmi}
        param['page']=page
        param['page_per_amount']=page_amount
        return self.perform_private(self.URL_HISTORY,param)
  
    def create_order(self,cmi,amount,ppc,category):
        param={'currency_market_id':cmi}
        param['amount']=amount
        param['ppc']=ppc
        param['category']=category
        return self.perform_private(self.URL_CREATE_ORDER,param)
  
    def delete_order(self,order_id):
        param={'order_id':order_id}
        return self.perform_private(self.URL_DELETE_ORDER,param)
  
    def delete_all_orders(self,cmi,category):
        param={'currency_market_id':cmi}
        param['category']=category
        return self.perform_private(self.URL_DELETE_ALL_ORDERS,param)
  
    def get_opened_markets(self):
        return self.perform_private(self.URL_OPENED_MARKETS)
  
    def get_currency_orders(self,cmi):
        param={'currency_market_id':cmi}
        return self.perform_private(self.URL_CURRENCY_ORDERS,param)
  
    def get_currency_trades(self,cmi,category,page=1,page_amount=20):
        param={'currency_market_id':cmi}
        param['page']=page
        param['page_per_amount']=page_amount
        param['category']=category
        return self.perform_private(self.URL_CURRENCY_TRADES,param)
  

  
