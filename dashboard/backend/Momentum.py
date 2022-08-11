"""
Calculates technical indicators for Microsoft (MSFT) stock

Robert Feliciano
"""
import datetime as dt
import requests_cache as cache
import numpy as np
import pandas as pd
import pandas_datareader as pdr
from pandas_datareader.yahoo.headers import DEFAULT_HEADERS

class Momentum:
    
    def __init__(self, ticker, start_dt, end_dt):
        #caching my resultss so I don't get IP banned. These will be erased from the directory 5 days after calling it for the first time
        expiration = dt.timedelta(days=5)
        self.session = cache.CachedSession(cache_name='cache', backend='sqlite', expire_after=expiration)
        self.session.headers = DEFAULT_HEADERS

        self.ticker = ticker
        self.start = start_dt
        self.end = end_dt
        
    """
    creates and returns a dataframe with columns:
        Adjusted Close
        MACD
        RSI
        Upper Bound of the Bollinger band
        Lower Bound of the Bollinger band
    """
    def calculateMomentumIndicators(self, lookback, window):
        """
        The dataframe will be null for some entries in every column other than adjusted close. This is 
        because of the periods and timeframes I chose to calculate the column's values with. For example,
        in the MACD column the first 26 entries are blank because I used a period of 26 days to base
        my exponential moving average on. I hope this is okay :)
        """
        start = lookback
        end = lookback + dt.timedelta(window*31) 
        #multiply the window by 31 so we get number of days in the window, since the window is given as 
        # an integer representing the number of months.
        df = pdr.DataReader(self.ticker, 'yahoo', start, end, session=self.session)
        self.calc_MACD(df)
        self.calc_RSI(df)

        upper_Bbound, lower_Bbound = self.calc_bollinger(df["Close"])
        df.insert(7, "Bollinger Upper Bound", upper_Bbound, True)
        df.insert(8, "Bollinger Lower Bound", lower_Bbound, True)

        #drop the columns we don't need
        df.drop('Close', axis=1, inplace=True)
        df.drop('Open', axis=1, inplace=True)
        df.drop('High', axis=1, inplace=True)
        df.drop('Volume', axis=1, inplace=True)
        df.drop('Low', axis=1, inplace=True)
        
        return df
        #for some reason the dataframe doesn't start at 01/01/2021, but instead starts at 01/04/2021.
        # I think this is because the market is closed on New Years Day (01/01) and then the next two days
        # were the weekend (01/02 and 01/03 were Saturday and Sunday, respectively)


    """
    #uses RSI values to create a strategy to buy or sell stocks. High RSI levels (above 70) indicate
    overbought stocks, which is a good time to sell. Low RSI levels (below 30) indicate
    oversold stocks, which is a good time to buy. I learned this from fidelity.com
    For the purposes of this, I will buy when RSI is below 35 for 2 days and sell when it above 65 for 2 days.
    For simplicity, I will use the Closing prices for my transactions.

    I think this is an effective strategy because it makes sense to buy when a stock is oversold, so its price is 
    lower than it should be and to sell when there is more demand for it (overbought) so its price is
    higher than it should be. 
    """
    def strategy(self):
        momentum = self.calculateMomentumIndicators(self.start, 6)
        rsi = momentum["RSI"].tolist()              #list of RSI values for the stock
        df = pdr.DataReader(self.ticker, 'yahoo', self.start, self.end, session=self.session)
        closing = df["Close"].tolist()              #list of closing prices
        dates = []
        types = []
        prices = []
        profits = []
        cumul_profits = []
        #all of the empty lists above will be populated with values as I use my trading algorithm and
        # then be inserted into a dataframe

        buy = True
        #"buy" is a flag that is set to true when I am allowed to buy a share, and false when I am not
        # I set it to false immediately after buying a share to indicate that the next action I can
        # do must be a sell
        below = 0
        above = 0
        for i in range(len(df)):
            if rsi[i] < 35:
                below+=1
            elif rsi[i] >64:
                above+=1
            if below >= 2 and rsi[i] < 35 and buy:
                date = str(df.index[i])
                dates.append(date[0:10])            #first 10 characters of the date is the yyyy-mm-dd
                types.append("BUY")
                prices.append(closing[i])
                profits.append(0)                   #I don't make any profit off a buy
                below = 0                           #Reset my RSI below 35 counter
                bought = i                          #Set an index called bought to indicate the last time I bought a stock
                buy = False                         #Now I HAVE to sell share.
            elif above >= 2 and rsi[i] > 65 and (not buy):
                date = str(df.index[i])
                dates.append(date[0:10])            #first 10 characters of the date is the yyyy-mm-dd
                types.append("SELL")
                prices.append(closing[i])
                p = closing[i] - closing[bought]    #Subtract price from when I last bought the share from the price at sell time
                profits.append(p)
                above = 0                           #Reset my RSI above 65 counter
                buy = True                          #Now I am allowed to buy a new share.

        cumul_profits = self.calc_cumulative_profits(cumul_profits, profits)
        #cumul_profits[-1] = cumul_profits[-1] + profits[-1] 
        
        ret_frame = pd.DataFrame()

        se = pd.Series(dates)
        ret_frame['Dates'] = se.values

        se = pd.Series(types)
        ret_frame['Transaction Type'] = se.values

        se = pd.Series(prices)
        ret_frame['Share Prices'] = se.values

        se = pd.Series(profits)
        ret_frame['Transaction Profits'] = se.values

        se = pd.Series(cumul_profits)
        ret_frame['Cumulative Profits'] = se.values

        return ret_frame
    

    def comparePerformance(self):
        #calculates the differences between using my strategy and just buying the stock at the beginning
        # of the 6 month period and selling it at the end
        df = pdr.DataReader(self.ticker, 'yahoo', self.start, self.end, session=self.session)
        open = df["Open"].tolist()              #list of opening prices
        close = df["Close"].tolist()            #list of closing prices

        #I am assuming the question wants us to buy it at the opening price of the first day and sell it at
        # the closing price of the final day.
        no_strategy = open[0] - close[len(close) - 1]

        sprofits = self.strategy()["Cumulative Profits"].tolist()
        strategy = sprofits[len(sprofits) - 1]

        return strategy - no_strategy
    
    """
    calculates 95% VaR, 95% CVaR, and Sharpe Ratio of my trading strategy's profits
    """
    def riskMetrics(self):
        profits = self.strategy()["Transaction Profits"]
        metrics = {}
        var95 = -1.65 * np.std(profits) 
        #95% variance is calculated to be -1.65 * standard deviation 
        metrics["95% VaR"] = var95

        cvar95 = -1.65 * np.std(profits)/np.mean(profits)
        metrics["95% CVaR"] = cvar95
        
        mean = profits.mean() * 255 -0.01
        sigma = profits.std() * np.sqrt(255)
        sharpe = mean/sigma
        metrics["Sharpe Ratio"] = sharpe
        #I do not know why the Sharpe ratio is so high... I am getting 8.9.
        # Maybe it is because the dataset is just very small? This is the only
        # method I could find online that didn't give me an error or a ratio of +/- infinity.
        # I spent about an hour and a half trying different ways I found online.
        
        return metrics


    """
    helper functions below
    """

    def calc_MACD(self, data):
        #calculating MACD. I am using the periods 12 and 26 because the finance websites I learned about MACD frmo said
        # said to use these periods. I guess I shouldn't question them.
        k = data['Close'].ewm(span=12, adjust=False, min_periods=12).mean()
        d = data['Close'].ewm(span=26, adjust=False, min_periods=26).mean()
        macd = k - d
        data['MACD'] = data.index.map(macd)

    def calc_RSI(self, data, periods = 5, ema = True):
        #Returns a pd.Series with the RSI. I used a period of 5 because when I looked up what period is best, finextra.com
        # said to use a period between 2-6. I am currently not in a place to question them.
        # As with calc_MACD, I will modify the existing datframe in place.
        close_delta = data['Close'].diff()

        # Make two series: one for lower closes and one for higher closes
        up = close_delta.clip(lower=0)
        down = -1 * close_delta.clip(upper=0)
        
        if ema:
            # Use exponential moving average
            ma_up = up.ewm(com = periods - 1, adjust=True, min_periods = periods).mean()
            ma_down = down.ewm(com = periods - 1, adjust=True, min_periods = periods).mean()
        else:
            # Use simple moving average
            ma_up = up.rolling(window = periods, adjust=False).mean()
            ma_down = down.rolling(window = periods, adjust=False).mean()
            
        rsi = ma_up / ma_down
        rsi = 100 - (100/(1 + rsi))
        data['RSI'] = data.index.map(rsi)

    """
    calculates both the Upper and Lower Bound of the Bollinger Band
    """
    def calc_bollinger(self, prices):
        #first we calculate the 20 day simple moving average
        # the dataframe will be null for the first 20 days because of this.
        sma = prices.rolling(20).mean()
        #next we calculate the standard deviation of every 20 day period
        std = prices.rolling(20).std() 
        #finally we calculate the bounds for the Bollinger Band
        b_up = sma + (std * 2)
        b_low = sma - (std * 2)
        return b_up, b_low

    def calc_cumulative_profits(self, cumul_profit, transactions):
        #at every index in profits, the cumulative profit is the sum of the values that come before
        # that index and the value at the index itself
        for i in range(len(transactions)):
            cumul_profit.append(sum(transactions[:i+1]))
        return cumul_profit


if __name__ == "__main__":
    ticker = "MSFT"
    start = dt.datetime(2021, 1, 1)
    end = dt.datetime(2021, 7, 1)
    window = 6 #6 months in example given in document
    m1 = Momentum(ticker, start, end)
    #df = m1.calculateMomentumIndicators(start, window)
    #df = m1.strategy()
    #print(df.to_string())
    #print(m1.riskMetrics())