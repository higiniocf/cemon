## Coin Exchange Monitor
## This examples use BTC/XP but can be used to monitor what ever you want. 
## Maintained by higinio
## Monitor Coin Exchange & Alert on specific conditions.

## Them Imports tho...
import requests
import json
import time
from datetime import datetime
from tzlocal import get_localzone

## New Variable Hotness...
xpLow = "0.00000014"     # Our Buy Point
xpHigh = "0.00000026"    # Our Sell Point!
xpPolling = 14           # Sleep Timer in  Seconds


def Get_CEMarket(id):
  #Attempt to hit the CE API Endpoint, on failure, fail gracefully.
    try:
      # Public Access URL to API 1
      url = 'https://www.coinexchange.io/api/v1/getmarketsummary?market_id=' + id
      #The API doesn't specify it but apparently not having a user agent gets your request blocked more often.
      headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
      # Create and Send GET request to our API Endpoint
      r = requests.get(url, headers=headers) 
      # Parse JSon
      data = json.loads(r.content)
    except:
      # Failed GET Request / JSON Parse. Lets fill it with useless information to so we may attempt again.
      data= {"success":"0","request":"\/api\/v1\/getmarket","message":"","result":{"MarketID":"0","LastPrice":"0","Change":"0","HighPrice":"0","LowPrice":"0","Volume":"0","BTCVolume":"0","TradeCount":"0","BidPrice":"0","AskPrice":"0","Bu$

    return data
def main():
    # Request Market Data for BTC/XP
    mrktData = Get_CEMarket('135')
    # Sort recieved Data from json.
    results = mrktData['success']                  # Success / Failure from API Endpoint (we simulate FAIL conditions when needed)
    lowPrice = mrktData['result']['LowPrice']      # LowPrice of Market
    highPrice = mrktData['result']['HighPrice']    # High Price of Market
    askPrice = mrktData['result']['AskPrice']      # Current Asking Price
    bidPrice = mrktData['result']['BidPrice']      # Current Bid Price
    changePrice = mrktData['result']['Change']     # The change of Market over the day
    Now = datetime.now(get_localzone()) 

    # Check to see if we got valid data from API End Point if we did then we evaluate on.
    if results == "1":       
       if askPrice <= xpLow:
        advice = "-BUY-"
       elif askPrice >= xpHigh:
        advice = "-SELl-"
       else:
        advice = "-STAY-"
       print '''
CEMON - BTC\XP {change} @ {ts}
Low: {low} High:{high}
Ask: {ask} Advice: {adv}'''.format(adv=advice,rs=results,low=lowPrice,high=highPrice,ask=askPrice,change=changePrice,ts=Now)
    return

#Main Loop
while True:
      main()
      time.sleep(xpPolling)
