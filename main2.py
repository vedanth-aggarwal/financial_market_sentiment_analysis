import requests
import streamlit as st
#from twilio.rest import Client
import pandas as pd
st.title('Company Financial Analysis')
#VIRTUAL_TWILIO_NUMBER = "your virtual twilio number"
#VERIFIED_NUMBER = "your own phone number verified with Twilio"

STOCK_NAME = "AAPL"
COMPANY_NAME = "Apple Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = ''
NEWS_API_KEY = ''
#TWILIO_SID = "YOUR TWILIO ACCOUNT SID"
#TWILIO_AUTH_TOKEN = "YOUR TWILIO AUTH TOKEN"

## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

#Get yesterday's closing stock price
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]

#print(yesterday_closing_price)

#Get the day before yesterday's closing stock price
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
#print(day_before_yesterday_closing_price)

#Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

#Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
diff_percent = round((difference / float(yesterday_closing_price)) * 100)
#print(diff_percent)
st.subheader('Stock News')
st.info(f'Percentage Difference - {diff_percent} {up_down}\n  Stock Yesterday - {yesterday_closing_price}\n  Stock Before Yesterday - {day_before_yesterday_closing_price}')
df = pd.DataFrame(data_list[:30])

# Rename columns to make them more readable
df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']

# Convert the columns to the appropriate data types
df['Open'] = df['Open'].astype(float)
df['High'] = df['High'].astype(float)
df['Low'] = df['Low'].astype(float)
df['Close'] = df['Close'].astype(float)
df['Volume'] = df['Volume'].astype(int)

# Display the DataFrame in Streamlit
st.dataframe(df)
st.line_chart(df['Volume'])
    ## STEP 2: Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

#Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.
#If difference percentage is greater than 5 then print("Get News").
if abs(diff_percent) > 1:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]

    #Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
    three_articles = articles[:3]
    print(three_articles)
    #print(three_articles)

    ## STEP 3: Use Twilio to send a seperate message with each article's title and description to your phone number.
    st.subheader('Global News')
    for article in three_articles:
        st.success(f'Title: {article['title']} \n  Brief: {article['description']}\n  Content:{article['content'][:200]} \n URL:{article['url']}')
    #Create a new list of the first 3 article's headline and description using list comprehension.
    formatted_articles = [f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
    #print(formatted_articles)
    #Send each article as a separate message via Twilio.
    
    from openai import OpenAI
    client = OpenAI(api_key='')
    
    #combined_text = ' '.join([article['title'] for article in news_articles])
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Your Job is to provide a structured financial market sentiment analysis and future prospects. Analyze financial data and external events to give a hollistic view"},
            {"role": "user", "content": f'News Articles:\n{formatted_articles}\nStock Prize Difference Yesterday: {diff_percent}\nPast Month Stock price: {data_list[:30]}'}
        ]
        )

    #sentiment = analyze_sentiment(combined_text)
    st.subheader('Market Analysis')
    st.warning(completion.choices[0].message.content)
    #print("\nMarket Sentiment Analysis:")
    #print(completion.choices[0].message.content)'''
    '''
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    
    #TODO 8. - Send each article as a separate message via Twilio.
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=VIRTUAL_TWILIO_NUMBER,
            to=VERIFIED_NUMBER
        )
    '''
