from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import json
import requests
import sys
import os
from forex_python.converter import CurrencyRates
from logdata import saveToDB

def getCoinList():
	api_key = "eb501339-9ae8-4687-beb5-27b0922be96d"
	base_domain = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=100"
	headers = {'Content-Type': 'application/json', 'X-CMC_PRO_API_KEY': api_key}

	response = requests.get(base_domain, headers=headers)
	if response.status_code == 200:
		return json.loads(response.content.decode('utf-8'))
	else:
		print(response.status_code)
		sys.exit()
		return None 

indxprice = 0
btcprice = 0
coinData = getCoinList()

# Forex rates
c = CurrencyRates()
forexRates = c.get_rates('USD')

# Print Date/Time
f=os.popen('date').read()
print(f)
print(forexRates)

# Calculate total from all coins
for d in coinData['data']:
	indxprice += float(d['quote']['USD'].get('market_cap'))
	if d['name'] == 'Bitcoin':
		btcprice = d['quote']['USD']['price']
	
# Ignore 0 prices
if indxprice == 0:
    sys.exit()
indxprice /= 100

# Divide by the total INDX supply
indxprice /= 1000000000.0

# Round return INDXcoin rate to 2 decimal places
indxprice = round(indxprice, 2)

#print(indxprice)

# Get diff if needed
#rpc_connection = AuthServiceProxy("http://%s:%s@seeder.indxcoin.org:3000"%("rpc", "sadfsadf"))
#difficulty = float(rpc_connection.getdifficulty())

marketcap = 1000000000 * indxprice
		
capobject = {
	'marketcap_USD': str(marketcap),
}
		
jsonPrice = json.dumps(capobject)
with open('marketcap.json', 'w') as f:
     json.dump(capobject, f)


shortData = {
    'INDX': indxprice,
    'USD': indxprice,
    'AUD': round(indxprice * forexRates['AUD'], 2),
    'EUR': round(indxprice * forexRates['EUR'], 2),
    'BRL': round(indxprice * forexRates['BRL'], 2),
    'CNY': round(indxprice * forexRates['CNY'], 2),
    'GBP': round(indxprice * forexRates['GBP'], 2),
    'HRK': round(indxprice * forexRates['HRK'], 2),
    'INR': round(indxprice * forexRates['INR'], 2),
    'RON': round(indxprice * forexRates['RON'], 2),
    'KRW': round(indxprice * forexRates['KRW'], 2)
}     
		
jsonPrice = json.dumps(shortData)
with open('shortData.json', 'w') as f:
     json.dump(shortData, f)

print(shortData)

saveToDB()