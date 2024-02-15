import pyautogui as pag
from datetime import timedelta
from pytz import timezone
import time
import datetime as dt
import Actions as act
import yfinance as yf 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dat = 'Datetime'
open = 'Open'
hi = 'High'
lo = 'Low'
close = 'Close'
adjclose = 'Adj Close'
vol = 'Volume'
df= pd.DataFrame()
xl= 'stonks.xlsx'
years = 15
endDate = dt.datetime.now()
startDate = endDate - dt.timedelta(days = 365*years)
tickerprim = "AAPL"
tickers = ['SPY']


def determine():
    recent_close = df.iloc[df.shape[0]-1,5]
    prev30_close = df.iloc[df.shape[0]-20,5]
    if(df.shape[0]>20):
        if(recent_close > prev30_close):
            return False
        elif(recent_close < prev30_close):
            return True

for ticker in tickers:
    data = yf.download(ticker, start = startDate, end = endDate)
    df[ticker] = data[adjclose]
    
    
log_returns = np.log(df/df.shift(1))
log_returns  = log_returns.dropna()
print(log_returns)

### Create a function that will be used to calculate portfolio expected return
#We are assuming that future returns are based on past returns, which is not a reliable assumption.
def expected_return(weights, log_returns):
    return np.sum(log_returns.mean()*weights)

### Create a function that will be used to calculate portfolio standard deviation
def standard_deviation (weights, cov_matrix):
    variance = weights.T @ cov_matrix @ weights
    return np.sqrt(variance)


### Create a covariance matrix for all the securities
cov_matrix = log_returns.cov()
print(cov_matrix)

### Create an equally weighted portfolio and find total portfolio expected return and standard deviation
portfolio_value = 1000000
weights = np.array([1/len(tickers)]*len(tickers))
portfolio_expected_return = expected_return(weights, log_returns)
portfolio_std_dev = standard_deviation (weights, cov_matrix)

def random_z_score():
    return np.random.normal(0, 1)

### Create a function to calculate scenarioGainLoss
days = 20

def scenario_gain_loss(portfolio_value, portfolio_std_dev, z_score, days):
    return portfolio_value * portfolio_expected_return * days + portfolio_value * portfolio_std_dev * z_score * np.sqrt(days)

### Run 10000 simulations
simulations = 10000
scenarioReturn = []

for i in range(simulations):
    z_score = random_z_score()
    scenarioReturn.append(scenario_gain_loss(portfolio_value, portfolio_std_dev, z_score, days))
    

### Specify a confidence interval and calculate the Value at Risk (VaR)
confidence_interval = 0.99
VaR = -np.percentile(scenarioReturn, 100 * (1 - confidence_interval))
print(VaR)

### Plot the results of all 10000 scenarios
""" plt.hist(scenarioReturn, bins=50, density=True)
plt.xlabel('Scenario Gain/Loss ($)')
plt.ylabel('Frequency')
plt.title(f'Distribution of Portfolio Gain/Loss Over {days} Days')
plt.axvline(-VaR, color='r', linestyle='dashed', linewidth=2, label=f'VaR at {confidence_interval:.0%} confidence level')
plt.legend()
plt.show() """

class MovingAverage:
    def __init__(self, window_size):
        self.window_size = window_size
        self.data = []

    def add_data_point(self, value):
        self.data.append(value)
        if len(self.data) > self.window_size:
            self.data.pop(0)

    def calculate_moving_average(self):
        if len(self.data) == 0:
            return 0  # Return 0 if there is no data
        return sum(self.data) / len(self.data)

# Fetch stock data for Apple Inc. (AAPL) from Yahoo Finance
symbol = "AAPL"

df = yf.download(symbol, startDate, endDate)

# Calculate moving average for the 'Close' column
window_size = 6
ma = MovingAverage(window_size)

for index, row in df.iterrows():
    ma.add_data_point(row['Close'])
    current_average = ma.calculate_moving_average()
    print(f"Date: {index}, Close Price: {row['Close']}, Moving Average: {current_average}")


""" 
i=True
while(i==True):
    c = 0
    act.auto_get_stock(tickerprim)
    df = pd.read_excel(xl)
    if(determine()==True):
        if(c<11):
            act.exec_trade(ticker)
            print(tickerprim, "bought")
            c+=1
        else:
            print("at trade limit no trade done")
    elif(determine()==False):
        act.sell_trade(tickerprim)
        print(ticker,"Sold")
        c-=1
    act.botpr("port.png")
    time.sleep(90)
 """