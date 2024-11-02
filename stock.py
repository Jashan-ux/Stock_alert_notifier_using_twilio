import requests
import os
from twilio.rest import Client

account_sid = 'AC29deef9xxxxxxxxxxxx528f76'
auth_token = 'afdcfc2747axxxxxxxxxx4823'
client = Client(account_sid, auth_token)


STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API_KEY ="MA92xxxxxxxx914ZMM"
NEWS_ENDPOINT = "Https://newsapi.org/v2/everything"
NEWS_API_KEY = "c3c639xxxxxxxxxxxxxxxx87fd8"
COMPANY_NAME = "Google"
STOCK_NAME = "GOOG"
stock_params = {
    "apikey": STOCK_API_KEY,
    "function" :"TIME_SERIES_DAILY",
    "symbol" : STOCK_NAME
    
}
news_params ={
    "apiKey" : NEWS_API_KEY,
    "qInTitle" : COMPANY_NAME
}
response = requests.get(STOCK_ENDPOINT , params=stock_params)
data = response.json()["Time Series (Daily)"]


data_list =[value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]


# day before yesterday's data
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]

# difference in price  b/w both days. absolute value in positive 
difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
up_down = None
if difference >0 :
    up_down = "🔺"
else:
    up_down = "🔻"
    
# % diff change 
percentage_diff = round(difference/float(yesterday_closing_price)*100,2)

#  if percentage greater than 5% print (get"news)


if abs(percentage_diff) >1 :
    response = requests.get(NEWS_ENDPOINT ,params=news_params)
    news_articles = response.json()["articles"]
    
    three_articles= news_articles[:3]
    formatted_articles =[f"{STOCK_NAME}: {up_down}{percentage_diff}% |\n Headline : {article['title']}. \nBrief: {article['description']}" for article in three_articles]

    
    
    for article in formatted_articles :
        message = client.messages.create(
        body = article ,
        from_='whatsapp:+141xxxx886',
        to='whatsapp:+9193xxxxxxxx10'
        )
        print(message.sid)
        










