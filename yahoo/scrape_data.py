import yfinance as yf

# Get the list of Dow 30 ticker symbols
tickers = [
    "AAPL", "MSFT" "AXP", "BA", "CAT", "CRM", "CSCO", "CVX", "DIS",
    "DOW", "GS", "HD", "HON", "IBM", "INTC", "JNJ", "JPM", "KO", "MCD",
    "MMM", "MRK", "MSFT", "NKE", "PG", "TRV", "UNH", "V", "VZ", "WBA", "WMT"
]

import pandas as pd
multi_data = yf.download(tickers, start="2009-01-01", end="2021-01-01")
print(multi_data.head() )
# Convert MultiIndex to columns
multi_data.columns = pd.MultiIndex.from_tuples(multi_data.columns)
df = multi_data.stack(level=1).reset_index()

# Rename columns
df.columns = ['Date', 'stock'] + list(df.columns[2:])

print(df.head())
print(df.columns)


df.to_csv("stock_data.csv")
