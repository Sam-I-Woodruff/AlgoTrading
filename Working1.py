
from dotenv import load_dotenv
import os
import requests
import json
import time
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

load_dotenv()

api_key = os.getenv('API_KEY')

tickers_df = pd.read_csv('C:\\Users\\samwo\\Documents\\Code\\Algo_Trading\\Tickers\\50Tickers.csv')

tickers = tickers_df['Tickers'].tolist()
print(tickers)

for ticker in tickers:
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&interval=5min&apikey={api_key}'
    response = requests.get(url)
    data = response.json()

    # Extracting time series data
    # time_series_key = "Time Series (Daily)"
    
    # if time_series_key in data:
    #     time_series = data[time_series_key]

    #     # Convert to DataFrame
    #     df = pd.DataFrame.from_dict(time_series, orient='index')
    #     df = df.astype(float)  # Convert string values to float
    #     df.index = pd.to_datetime(df.index)  # Convert index to datetime
    #     df.sort_index(inplace=True)  # Ensure correct order

    #     # Plot closing prices
    #     plt.figure(figsize=(10, 5))
    #     plt.plot(df.index, df['4. close'], marker='o', linestyle='-')
    #     plt.xlabel('Date')
    #     plt.ylabel('Close Price')
    #     plt.title(f'Closing Prices for {ticker}')
    #     plt.xticks(rotation=45)
    #     plt.grid()

    #     # Show the plot
    #     plt.show()

# print(data['Time Series (5min)'])

    print(json.dumps(data, indent=4))
    time.sleep(15)