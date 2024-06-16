import pandas as pd
import yfinance as yf

# tickers = # Get the list of Dow 30 ticker symbols
tickers = [
    "AAPL", "MSFT" "AXP", "BA", "CAT", "CRM", "CSCO", "CVX", "DIS",
    "DOW", "GS", "HD", "HON", "IBM", "INTC", "JNJ", "JPM", "KO", "MCD",
    "MMM", "MRK", "MSFT", "NKE", "PG", "TRV", "UNH", "V", "VZ", "WBA", "WMT"
]



data_dict = {"stock": [], "longBusinessSummary": [], "overallRisk": []}
for ticker in tickers:
    stock = yf.Ticker(ticker)
    info = stock.info
    print(info)

    if info is not None:
        #update data_dict with info
        data_dict['stock'].append(ticker)
        if 'longBusinessSummary' in info.keys():
          data_dict['longBusinessSummary'].append(info['longBusinessSummary']) 
          data_dict['overallRisk'].append(info['overallRisk'])
        else:
          data_dict['longBusinessSummary'].append("") 
          data_dict['overallRisk'].append(10)

df = pd.DataFrame(data_dict)
df.to_csv('companies_info.csv')

print(df.head())