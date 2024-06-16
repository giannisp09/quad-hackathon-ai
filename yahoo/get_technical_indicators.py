import pandas as pd
import talib

# Load the dataset
file_path = 'stock_data.csv'
data = pd.read_csv(file_path)


# Ensure the data is sorted by date and includes a stock identifier
data['Date'] = pd.to_datetime(data['Date'])
data.sort_values(by=['stock', 'Date'], inplace=True)

# Define a function to calculate indicators for each stock
def calculate_indicators(stock_data):
    stock_data['MACD'], stock_data['MACD_Signal'], stock_data['MACD_Hist'] = talib.MACD(stock_data['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
    stock_data['RSI'] = talib.RSI(stock_data['Close'], timeperiod=14)
    stock_data['CCI'] = talib.CCI(stock_data['High'], stock_data['Low'], stock_data['Close'], timeperiod=14)
    stock_data['ADX'] = talib.ADX(stock_data['High'], stock_data['Low'], stock_data['Close'], timeperiod=14)
    return stock_data

# Apply the function to each group of stocks
data = data.groupby('stock').apply(calculate_indicators)

# Reset index after groupby operation
data.reset_index(drop=True, inplace=True)

# Columns to backfill
columns_to_backfill = ['MACD', 'MACD_Signal', 'MACD_Hist', 'RSI', 'CCI', 'ADX']

# Perform backfill on the selected columns
data[columns_to_backfill] = data.groupby('stock')[columns_to_backfill].apply(lambda group: group.fillna(method='bfill'))

# Save the backfilled dataframe to a new CSV file
output_file_path_bfill = 'stock_data_ti.csv'
data.to_csv(output_file_path_bfill, index=False)