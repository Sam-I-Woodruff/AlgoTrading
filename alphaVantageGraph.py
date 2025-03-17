import pandas as pd
import matplotlib.pyplot as plt
import os

# Path to your tickers folder
tickerpath = "C:\\Users\\samwo\\Documents\\Code\\Algo_Trading\\Tickers\\"

# List of ticker files
ticker_files = [f for f in os.listdir(tickerpath) if f.endswith(".csv")]

# Loop through each ticker file and plot
for file in ticker_files:
    file_path = os.path.join(tickerpath, file)
    
    # Read the CSV file
    df = pd.read_csv(file_path, names=["Date", "Close"], parse_dates=["Date"])
    
    # Sort data by date (in case it's not sorted)
    df = df.sort_values("Date")

    # Plot the data
    plt.figure(figsize=(10, 5))
    plt.plot(df["Date"], df["Close"], label=file.replace(".csv", ""), marker="o", linestyle="-")

    # Formatting
    plt.xlabel("Date")
    plt.ylabel("Closing Price")
    plt.title(f"Stock Price for {file.replace('.csv', '')}")
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid()

    # Show the plot
    plt.show()
