import json

"""
converts from string to json format, and then finds the symbols and open/close values in json data
returns dictionary of oepn/close prices for the stock(s)
"""
def json_parser(jlist):
    prices = dict()
    #print(jlist)
    for j in jlist:
        stock_dict = json.loads(j)
        prices[stock_dict.get('symbol')] = [stock_dict.get('open'), stock_dict.get('close')]
    #print(prices.get('AAPL')[0])
    return prices
    


#print(json_parser(['{"status":"OK","from":"2021-08-20","symbol":"AAPL","open":147.44,"high":148.5,"low":146.78,"close":148.19,"volume":60249630,"afterHours":148.31,"preMarket":146}']).get('AAPL')[0])