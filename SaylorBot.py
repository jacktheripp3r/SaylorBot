#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tweepy
import requests
import base64
import time
import locale
import os 
from os import environ 

# In[2]:


api = environ['api']
api_secret = environ['api_secret']
api_bearer = environ['api_bearer']
accesstoken = environ['accesstoken']
accesssecrettoken = environ['accesssecrettoken']
cmcapi = environ['cmcapi']

#authenticating to access the twitter API
auth=tweepy.OAuthHandler(api,api_secret)
auth.set_access_token(accesstoken,accesssecrettoken)
api=tweepy.API(auth)

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': cmcapi,
}

session = requests.Session()
session.headers.update(headers)

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
response = session.get(url)

while True:
    def human_format(num):
        num = float('{:.5g}'.format(num))
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
        return '${} {}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'Mn', 'Bn', 'Tn'][magnitude])
    ltp = round(response.json()['data'][0]['quote']['USD']['price'], 2)
    average = 27713
    quantity = 114042
    
    pl = ltp - average
    investment = human_format(average*quantity)
    finalpl = human_format(pl * quantity)
    percentreturn = human_format(((pl)/average)*100).replace('$', '')
    percentreturn = percentreturn.replace(' ','')
    if pl > 0:
        percentreturn = '+' + percentreturn
    else:
        percentreturn = '-' + percentreturn
    tweet = f'Michael Saylor\'s Bitcoin Average: ~${average}\n\nProfit/Loss: {finalpl}({percentreturn}%)\n\nBitcoin Hodled: ~₿{quantity}\n\nTotal Investment: {investment}\n\nLearn from the Gigachad. Keep Stacking Sats.\n\n#Bitcoin'
    api.update_status(tweet)
    time.sleep(1800)

