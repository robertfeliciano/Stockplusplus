import requests
#from dashboard import key_vault

#key = key_vault.api_key

url = 'https://api.polygon.io'

'''
Takes ticker symbols and dates as inputs; outputs list containing the following:
    list of json data for each stock in the inputs
'''
def daily_info(tickers, date):
    json_vals = []
    #print(tickers)
    for ticker in tickers:
        endpoint = f'{url}/v1/open-close/{ticker}/{date}?adjusted=true&apiKey={key}'
        response = requests.get(endpoint)
        json_vals.append(response.text)
    return json_vals


#print(daily_info(['GOOG'], '2021-08-20'))
