import pandas as pd

def turtle_trading_strategy(data, n):
    data['High_' + str(n)] = data['High'].rolling(n).max()
    data['Low_' + str(n)] = data['Low'].rolling(n).min()
    data['Buy'] = data['Close'] > data['High_' + str(n)].shift(1)
    data['Sell'] = data['Close'] < data['Low_' + str(n)].shift(1)
    return data

# Load historical stock data from a CSV file
df = pd.read_csv('stock_data.csv')

# Apply the Turtle Trading strategy with a parameter value of 20
df = turtle_trading_strategy(df, 20)

# Filter the DataFrame to include only the relevant columns
df = df[['Date', 'Close', 'Buy', 'Sell']]

# Iterate over the rows to simulate trading and calculate profits
capital = 10000  # Initial capital
shares = 0       # Number of shares held
for index, row in df.iterrows():
    if row['Buy']:
        shares = capital / row['Close']
        capital = 0
    elif row['Sell']:
        capital = shares * row['Close']
        shares = 0

# Calculate the final portfolio value
portfolio_value = capital + (shares * df.iloc[-1]['Close'])

print("Final Portfolio Value: $", portfolio_value)
