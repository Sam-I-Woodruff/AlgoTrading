import requests
import json
import time
import os
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi

load_dotenv()

api_key = os.getenv('API_KEY2')
api_secret = os.getenv('API_SECRET2')
base_url = 'https://paper-api.alpaca.markets'

def alpacaBuy(t):
    api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')
    try:
        order = api.submit_order(
            symbol=t,
            qty=1,
            side='buy',
            type='market',
            time_in_force='gtc'
        )
    except:
        print('order failed')
        
    
def alpacaSell(t):
    api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')
    
    try:
        order = api.submit_order(
            symbol=t,
            qty=1,
            side='sell',
            type='market',
            time_in_force='gtc'
        )
    except:
        print('order failed')
    

def bollingerBandsStrategy(prices, t):
    buy = 0
    first_buy = 0
    profit = 0
    profit_each = 0
    five_day_average = 0
    buy_checker = 0
    sell = 0
    statement = 0
    statement_boolean = True
    shorting = True 

    for i in range(count): #looping through all indeces of prices
        if i >= 5: #Has moving average initiate at index 0
            current_price = prices[i] #resets price for each loop iteration 
            five_day_average = (prices[-1+i] + prices[-2+i] + prices[-3+i] + prices[-4+i] + prices [-5+i])/5 #calculates 5-day moving average
            if current_price > (five_day_average * 1.04) and buy == 0: #buy for SMA
                if current_price == prices[5]: #uses the first iteration from our csv list of prices to get today's price.
                    alpacaBuy(t)
                if buy_checker == 0: #steps into if first buy
                    first_buy = current_price
                    buy_checker = 1 #sets aspect to only sell after getting first
                buy = current_price #performs buying aspect
                print("Buy at: ", round(buy, 2))
                if buy != 0 and sell != 0 and shorting: #condition for shorting
                    profit += sell - buy #calculates shorting profit
                    print("Trade Profit = ", round((sell-buy), 2))
                sell = 0 #reseting variable for
                if statement == (count):#buy or sell conditional on last day
                    statement_boolean = True #print buy this stock
            elif current_price < (five_day_average * 0.96) and buy != 0: #sell for SMA
                if current_price == prices[5]: #uses the first iteration from our csv list of prices to get today's price.
                    alpacaSell(t)
                sell = current_price
                print("Sell at: ", round(current_price, 2))
                if buy != 0 and sell != 0: #condition for shorting
                    profit += sell - buy #calculates shorting profit
                    print("Trade Profit = ", round((sell-buy), 2))
                profit += (current_price - buy)  #calculates profit without shorting
                profit_each = current_price - buy
                buy = 0; #sets buying aspect possible again
                print("Trade Profit = ", round(profit_each, 2))
                if statement == (count): #buy or sell conditional on last day
                    statement_boolean = False #print sell this stock
            else:
                pass
    
    final_profit_percentage = round((profit/first_buy) * 100, 2) #calcs profit percentage
    print("---------------------------------\nTotal profit: ", round(profit, 2))
    print("First Buy: ", round(first_buy, 2))
    print("Percentage Return: ", (final_profit_percentage), "%\n\n\n")
    return profit, final_profit_percentage #returns both variables in the function

#calculates the mean reversions strategy of a 5-day moving average
def meanReversionStrategy(prices, t):
    # establishing all variables below
    buy = 0
    first_buy = 0
    profit = 0
    profit_each = 0
    five_day_average = 0
    buy_checker = 0
    buy_today = 0
    
    for i in range(count): #looping through all indeces of prices
        if i >= 5: #Has moving average initiate at index 0
            current_price = prices[5] #resets price for each loop iteration 
            five_day_average = (prices[-1+i] + prices[-2+i] + prices[-3+i] + prices[-4+i] + prices [-5+i])/5 #calculates 5-day moving average
            if current_price < five_day_average * .98 and buy == 0: #buy
                if current_price == prices[5]: #uses the first iteration from our csv list of prices to get today's price.
                    alpacaBuy(t)
                if buy_checker == 0: #steps into if first buy
                    first_buy = current_price
                    buy_checker = 1 #assigns sentinal for this if statemtn
                buy = current_price #performs buying aspect
                print("Buy at: ", round(buy, 2))
            elif current_price > five_day_average * 1.02 and buy != 0: #sell
                if current_price == prices[5]: #uses the first iteration from our csv list of prices to get today's price.
                    alpacaSell(t)
                profit += (current_price - buy)  #calculates total profit
                profit_each = current_price - buy 
                buy = 0; #allows aspect of buying again
                print("Sell at: ", round(current_price, 2))
                print("Trade Profit = ", round(profit_each, 2))
            else:
                pass
    
    final_profit_percentage = round((profit/first_buy) * 100, 2) #calcs profit percentage
    print("---------------------------------\nTotal profit: ", round(profit, 2))
    print("First Buy: ", round(first_buy, 2))
    print("Percentage Return: ", (final_profit_percentage), "%\n\n\n")
    return profit, final_profit_percentage #returns both variables in the function
    
    
def simpleMovingAverageStrategy(prices, t): #currently has shorting
    buy = 0
    first_buy = 0
    profit = 0
    profit_each = 0
    five_day_average = 0
    buy_checker = 0
    sell = 0
    statement = 0
    statement_boolean = True
    shorting = True 

    for i in range(count): #looping through all indeces of prices
        if i >= 5: #Has moving average initiate at index 0
            current_price = prices[i] #resets price for each loop iteration 
            five_day_average = (prices[-1+i] + prices[-2+i] + prices[-3+i] + prices[-4+i] + prices [-5+i])/5 #calculates 5-day moving average
            if current_price > five_day_average and buy == 0: #buy for SMA
                if current_price == prices[5]: #uses the first iteration from our csv list of prices to get today's price.
                    alpacaBuy(t)
                if buy_checker == 0: #steps into if first buy
                    first_buy = current_price
                    buy_checker = 1 #sets aspect to only sell after getting first
                buy = current_price #performs buying aspect
                print("Buy at: ", round(buy, 2))
                if buy != 0 and sell != 0 and shorting: #condition for shorting
                    profit += sell - buy #calculates shorting profit
                    print("Trade Profit = ", round((sell-buy), 2))
                sell = 0 #reseting variable for
                if statement == (count):#buy or sell conditional on last day
                    statement_boolean = True #print buy this stock
            elif current_price < five_day_average and buy != 0: #sell for SMA
                if current_price == prices[5]: #uses the first iteration from our csv list of prices to get today's price.
                        alpacaSell(t)
                sell = current_price
                print("Sell at: ", round(current_price, 2))
                if buy != 0 and sell != 0: #condition for shorting
                    profit += sell - buy #calculates shorting profit
                    print("Trade Profit = ", round((sell-buy), 2))
                profit += (current_price - buy)  #calculates profit without shorting
                profit_each = current_price - buy
                buy = 0; #sets buying aspect possible again
                print("Trade Profit = ", round(profit_each, 2))
                if statement == (count): #buy or sell conditional on last day
                    statement_boolean = False #print sell this stock
            else:
                pass
    
    final_profit_percentage = round((profit/first_buy) * 100, 2) #calcs profit percentage
    print("---------------------------------\nTotal profit: ", round(profit, 2))
    print("First Buy: ", round(first_buy, 2))
    print("Percentage Return: ", (final_profit_percentage), "%\n\n\n")
    return profit, final_profit_percentage #returns both variables in the function


def saveResults(dictionary): #convert dictionary to json file
    json.dump(dictionary, open("/home/ubuntu/environment/Final_Project/results.json", "w"), indent = 4) 
    #performs dump function to create json file from dictionary in hw5 folder


tickers = ['BABA', 'CSCO', 'BAC', 'KSS', 'AMZN', 'AAPL', 'GOOG', 'ADBE', 'GME', 'BA'] #assigns all tickers
results = {} #establish dict

# getStockData(tickers) #Use to get the original stock data
# appendStockData(tickers) #ran to iterate through and -------------------------------------------------------- uncomment when done ---------------------------------------------------------------------------------------------------------------------

# alpacaBuy('BABA')

for i in tickers: #iterates through each ticker
    
    file = open("/home/ubuntu/environment/Final_Project/data/%s.csv"%(i))
    lines = file.readlines() 
    
    prices = []
    for line in lines:
        prices.append(float(line.split(",")[1]))
        
    # results["%s_prices"%(i)] = prices
    
    # total = 0
    count = 0
    for price in prices: #counts variable to give range in for loop with functions
        count += 1
    #     total += price
    # avg = total/count
    # print("totale average price: ", avg)
    
    print(i, " Mean Reversion Strategy")
    mrprofit, mrreturns = meanReversionStrategy(prices, i)
    
    print(i, " Simple Moving Average Strategy")
    smaprofit, smareturns = simpleMovingAverageStrategy(prices, i)
    
    print(i, " Bollinger Bands Strategy")
    bbprofit, bbreturns = bollingerBandsStrategy(prices, i)
    
    results['%s_mr_profit'%(i)] = mrprofit
    results['%s_mr_returns'%(i)] = mrreturns
    
    results['%s_sma_profit'%(i)] = smaprofit
    results['%s_sma_returns'%(i)] = smareturns
    
    results['%s_bb_profit'%(i)] = bbprofit
    results['%s_bb_returns'%(i)] = bbreturns

saveResults(results)
input("press any key")