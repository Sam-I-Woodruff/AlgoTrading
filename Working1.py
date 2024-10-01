
from dotenv import load_dotenv
import os
import requests
import json
import time
import pandas as pd
from datetime import datetime, timedelta

load_dotenv()

api_key = os.getenv('API_KEY')

tickers_df = pd.read_csv('C:\\Users\\samwo\\Documents\\Code\\Algo_Trading\\50Tickers.csv')

tickers = tickers_df['Tickers'].tolist()
print(tickers)

for ticker in tickers:
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&interval=5min&apikey={api_key}'
    response = requests.get(url)
    data = response.json()

# print(data['Time Series (5min)'])

    print(json.dumps(data, indent=4))
    time.sleep(15)