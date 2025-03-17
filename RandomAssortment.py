
from dotenv import load_dotenv
import os
import requests
import json
import time
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

load_dotenv()

api_key = os.getenv('API_KEY2')

tickers_df = pd.read_csv('C:\\Users\\samwo\\Documents\\Code\\Algo_Trading\\Tickers\\RealTickers.csv')

tickers = tickers_df['Tickers'].tolist()
print(tickers)

tickerpath = "C:\\Users\\samwo\\Documents\\Code\\Algo_Trading\\Tickers\\"

for ticker in tickers:
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&interval=5min&apikey={api_key}'
    response = requests.get(url)
    req_dict = json.loads(response.text)

    key1 = "Time Series (Daily)" # dictionary with all prices by date
    key2 = '4. close'

    file_path = os.path.join(tickerpath, f"{ticker}.csv")

    data = response.json()

    #Checking if file exists and/or is empty
    if not os.path.exists(file_path):
        print("File does not exist, and will be created later")
    else: #Seeing how big the file is
        csv_file = open(file_path)
        lines = csv_file.readlines()
        last_date = lines[-1].split(",")[0]

        size = os.path.getsize(file_path)
        if size == 0: # file exists, but is empty
            print("file exists, but is empty")
        else:
            print(f"Size of file {ticker}.csv is {size}")
    
    
    new_lines = []
    for date in req_dict[key1]:
        if date == last_date:
            break
        #print(date + "," + req_dict[key1][date][key2]) #print key, value
        new_lines.append(date + "," + req_dict[key1][date][key2]+"\n")
        
    new_lines = new_lines[::-1]
    csv_file = open(file_path, "a") # opening the file to append data
    csv_file.writelines(new_lines) # appending new data
    csv_file.close()

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