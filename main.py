import requests
from twilio.rest import Client


STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

VIRTUAL_TWILIO_NUMBER = ""
VERIFIED_NUMBER = ""

TWILIO_SID = ""
TWILIO_AUTH_TOKEN = ""

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

NEWS_KEY = ""
ALPHA_KEY = ""


stock_parameters = {
    "symbol": STOCK_NAME,
    "apikey": ALPHA_KEY,
    "function": "TIME_SERIES_DAILY"
}


# get a response from the api , then turn it into JSON
response = requests.get(STOCK_ENDPOINT, params=stock_parameters)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]



day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]


difference = abs(float(yesterday_closing_price) - float(day_before_yesterday_closing_price))
print(difference)
up_down = None
if difference > 0:
    up_down = "UP"
else:
    up_down = "DOWN"


diff_percent = difference / float(yesterday_closing_price) * 100
print(diff_percent)



if diff_percent > 1:
    news_parameters = {
        "apiKey": NEWS_KEY,
        "qInTitle": COMPANY_NAME,

    }


    news_response = requests.get(NEWS_ENDPOINT, params=news_parameters)
    articles = news_response.json()["articles"]



    three_articles = articles[:3]
    print(three_articles)



    formatted_articles = [f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
    print(formatted_articles)
    #Send each article as a separate message via Twilio.
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=VIRTUAL_TWILIO_NUMBER,
            to="YOUR_NUMBER"
        )