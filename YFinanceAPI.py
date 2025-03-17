import yfinance as yf
import pandas as pd
import time
import os

# Define the date range
start_date = '2014-09-30'
end_date = '2024-09-30'

folder_path = 'C:\\Users\\samwo\\Documents\\Code\\Algo_Trading\\YFinanceTenYears\\'
tickers_df = pd.read_csv('C:\\Users\\samwo\\Documents\\Code\\Algo_Trading\\Tickers\\50Tickers.csv')
tickers = tickers_df['Tickers'].tolist()

failed_tickers = []

for ticker in tickers:
    try:
        # Fetch historical data
        data = yf.download(ticker, start=start_date, end=end_date, interval='1d', progress=False)

        # Check if data is empty
        if data.empty:
            print(f"Failed to download: {ticker} (empty data)")
            failed_tickers.append(ticker)
            continue

        # Save to CSV
        csv_path = os.path.join(folder_path, f'{ticker}_daily_data.csv')
        data.to_csv(csv_path)
        print(f"Saved {ticker} data to {csv_path}")

    except Exception as e:
        print(f"Failed to get ticker '{ticker}' due to: {e}")
        failed_tickers.append(ticker)

    # Pause to prevent rate limiting
    time.sleep(2)

# Log failed tickers
if failed_tickers:
    print("\nFailed tickers:", failed_tickers)
