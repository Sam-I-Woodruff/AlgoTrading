import requests
import json
import time
from datetime import datetime, timedelta


def GetNewCryptoData(coins):
    dt = datetime(2021, 4, 21)
    count = 0

    for coin in coins:
        file = open("/home/ec2-user/environment/Final_Project/" + coin + ".csv", "w")
        file.write("Date," + coin + "\n")
        for i in range(364):
            dt += timedelta(days=1) #increases day by 1
            count += 1
            dts = dt.strftime("%d-%m-%Y")
            url = url1 + coin + url2 + dts + url3 #concatenates API url
            req = requests.get(url)
            time.sleep(1)
            d = json.loads(req.text)
            try: #attempts to run code and handles exceptions
                print(dts, d[key1][key2][key3])
                file.write(dts + "," + str(d[key1][key2][key3]) + "\n") #writes to the file the data
            except:
                pass
                print(d)
        dt -= timedelta(days=364) #Reseting the date for each ticker. Days has to equal range limit
    file.close()
    

def AppendCryptoData(coins):
    dt = datetime(2022, 5, 3) #will use date simply to always have a date farther back than latest currency grab
    date_counter = 0 #counter to reset date variable through each iteration
    
    
    for coin in coins:
        file = open("/home/ec2-user/environment/Final_Project/" + coin + ".csv", "r")
        # file.write("Date," + coin + "\n")
        last_date_str = file.readlines()[-1].split(",")[0] #grabs the last date in the file
        last_dt = datetime.strptime(last_date_str, '%d-%m-%Y')
        current_date = datetime.now() #sets the current date
        
        file.close()
        file = open("/home/ec2-user/environment/Final_Project/" + coin + ".csv", "a")
        for i in range(364):
            dt += timedelta(days=1) #adds 1 to the date each iteration
            date_counter += 1
            if dt > current_date: #checks if it's in the future/date doesn't exist
                break
            
            dts = dt.strftime("%d-%m-%Y")
            url = url1 + coin + url2 + dts + url3 #concatenates url
            req = requests.get(url)
            time.sleep(1)
            d = json.loads(req.text)
            
            try:
                print(dts, d[key1][key2][key3])
                if dt > last_dt and dt <= current_date: #checks to see if date is valid for our data
                    file.write(dts + "," + str(d[key1][key2][key3]) + "\n") #writes to file
                    
            except:
                pass
                # print(d)
        dt -= timedelta(days=(date_counter)) #Reseting the date for each ticker. Days has to equal range limit. Needs to be 
        date_counter = 0
    file.close()


#calculates the mean reversions strategy of a 5-day moving average
def meanReversionStrategy(prices):
    # establishing all variables below
    buy = 0
    first_buy = 0
    profit = 0
    profit_each = 0
    five_day_average = 0
    buy_checker = 0
    statement = 0
    statement_boolean = True
    
    for i in range(count): #looping through all indeces of prices
        if i >= 5: #Has moving average initiate at index 0
            current_price = prices[i] #resets price for each loop iteration 
            five_day_average = (prices[-1+i] + prices[-2+i] + prices[-3+i] + prices[-4+i] + prices [-5+i])/5 #calculates 5-day moving average
            if current_price < five_day_average * .98 and buy == 0: #buy
                if buy_checker == 0: #steps into if first buy
                    first_buy = current_price
                    buy_checker = 1 #assigns sentinal for this if statemtn
                buy = current_price #performs buying aspect
                print("Buy at: ", round(buy, 2))
                if statement == (count): #buy or sell conditional on last day
                    statement_boolean = True
            elif current_price > five_day_average * 1.02 and buy != 0: #sell
                profit += (current_price - buy)  #calculates total profit
                profit_each = current_price - buy 
                buy = 0; #allows aspect of buying again
                print("Sell at: ", round(current_price, 2))
                print("Trade Profit = ", round(profit_each, 2))
                if statement == (count): #buy or sell conditional on last day
                    statement_boolean = False
            else:
                pass
        statement += 1
    
    if statement_boolean:
        print("buy this stock today")
    else:
        print("sell this stock today")
    final_profit_percentage = round((profit/first_buy) * 100, 2) #calcs profit percentage
    print("---------------------------------\nTotal profit: ", round(profit, 2))
    print("First Buy: ", round(first_buy, 2))
    print("Percentage Return: ", (final_profit_percentage), "%\n\n\n")
    return profit, final_profit_percentage #returns both variables in the function
    
    
def simpleMovingAverageStrategy(prices):
    buy = 0
    first_buy = 0
    profit = 0
    profit_each = 0
    five_day_average = 0
    buy_checker = 0
    sell = 0
    statement = 0
    statement_boolean = True
    shorting = True #used to test with or without shorting as a test variable

    for i in range(count): #looping through all indeces of prices
        if i >= 5: #Has moving average initiate at index 0
            current_price = prices[i] #resets price for each loop iteration 
            five_day_average = (prices[-1+i] + prices[-2+i] + prices[-3+i] + prices[-4+i] + prices [-5+i])/5 #calculates 5-day moving average
            if current_price > five_day_average and buy == 0: #buy for SMA
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
    
    if statement_boolean:
        print("buy this stock today")
    else:
        print("sell this stock today")
    final_profit_percentage = round((profit/first_buy) * 100, 2) #calcs profit percentage
    print("---------------------------------\nTotal profit: ", round(profit, 2))
    print("First Buy: ", round(first_buy, 2))
    print("Percentage Return: ", (final_profit_percentage), "%\n\n\n")
    return profit, final_profit_percentage #returns both variables in the function


def saveResults(dictionary): #convert dictionary to json file
    import json
    json.dump(dictionary, open("/home/ec2-user/environment/Final_Project/results.json", "w"), indent = 4) 
    #performs dump function to create json file from dictionary in hw5 folder
    
    
    
url = "https://api.coingecko.com/api/v3/coins/bitcoin/history?date=30-11-2020&localization=false"
req = requests.get(url)

url1 = "https://api.coingecko.com/api/v3/coins/"
url2 = "/history?date="
url3 = "&localization=false"

key1 = 'market_data'
key2 = 'current_price'
key3 = 'usd'


coins = ["bitcoin-cash", "eos", "litecoin", "ethereum", "bitcoin"]
count = 0

AppendCryptoData(coins); #gets new data

results = {} #establish dict
for i in coins: #iterates through each ticker

    
    prices = [float(line.split(",")[1]) for line in open("/home/ec2-user/environment/Final_Project/" + i + ".csv", "r").readlines()[1:]]
        
    results["%s_prices"%(i)] = prices #sets list to the prcies for each ticker
    
    for price in prices: #counts variable to give range in for loop with functions
        count += 1
    
    print(i, " Mean Reversion Strategy")
    mrprofit, mrreturns = meanReversionStrategy(prices) #runs mean reversion strategy
    
    print(i, " Simple Moving Average Strategy")
    smaprofit, smareturns = simpleMovingAverageStrategy(prices) #runs simple moving average strategy
    
    #the next 4 lines save data to the dictionary with each specific key
    results['%s_mr_profit'%(i)] = mrprofit
    results['%s_mr_returns'%(i)] = mrreturns
    
    results['%s_sma_profit'%(i)] = smaprofit
    results['%s_sma_returns'%(i)] = smareturns
    
    count = 0 #resets count variable for the interation

saveResults(results) #runs function to dump dict as a json file
input("press any key") #wait for file to load all data before closing