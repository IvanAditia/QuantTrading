from unittest import result
import pandas as pd
import ta

# PATH

PATH = "../data/raw/GC=F_1m.csv"
df = pd.read_csv(PATH)

# INDICATOR

df['mean'] = df['Close'].rolling(14).mean() 

df['standar_deviation'] = df['Close'].rolling(14).std()

df['adx'] = ta.trend.ADXIndicator(
    high=df['High'],
    low=df['Low'],
    close=df['Close'],
    window=14
).adx()

position = 0
entry_price = 0
initial_balance = 100
balance = initial_balance

trade = []


# KRITERIA CANDLE

df['body'] = abs(df['Close'] - df['Open'])

df['range_body'] = (df['body'] >= 5)  & (df['body'] <= 20)

df['bull_candle'] = df['Close'] > df['Open'] 

df['bear_candle']  = df['Close'] < df['Open']

df['upper_wick'] = df['High'] - df[['Open', 'Close']].max(axis=1)

df['upper_wick_range'] = df['upper_wick']  <= (df['body'] * 0.05)

df['Lower_wick'] = df[['Open', 'Close']].min(axis=1) - df['Low']

df['Lower_wick_range'] = df['Lower_wick'] <= (df['body'] * 0.05) 

df['prev_candle_bull'] = df['Close'].shift(1) > df['Open'].shift(1)

df['prev_candle_bear'] = df['Close'].shift(1) < df['Open'].shift(1)



# SIGNAL

df['buy_entry'] = (
    (df['Close'] > df['mean']) &
    (df['range_body']) &
    (df['upper_wick_range']) &
    (df['prev_candle_bull']) &
    (df['adx'] >= 16)
)   



df['sell_entry'] = (
    (df['Close'] < df['mean']) & 
    (df['range_body']) &
    (df['Lower_wick_range']) &
    (df['prev_candle_bear']) &
    (df['adx'] >= 16)
)

# BACKTEST LOOPING

for i in range(14, len(df)):
    price = df['Close'].iloc[i]

    # ENTRY
    if position == 0:
        if df['buy_entry'].iloc[i]:
            position = 1
            entry_price = price
            trade.append({
                'type' : 'BUY', 
                'price' :price,
                'index' :  i
            })

        elif df['sell_entry'].iloc[i]:
            position = -1
            entry_price = price
            trade.append({
                'type' : 'SELL',
                'price' : price,
                'index' : i
            })

        elif df['adx'].iloc[i] <= 15 :
            position = 0

    # EXIT, SL, TP
    elif position == 1 :
        sl_price = entry_price - df['standar_deviation'].iloc[i]
        tp_price = entry_price + (2 * df['standar_deviation'].iloc[i])

        if df['Low'].iloc[i] <= sl_price  :            
            profit = sl_price - entry_price
            balance += profit
            trade.append({
                'type' : 'BUY SL',
                'price' : sl_price,
                'index' : i,
                'profit' : profit
            })
            position = 0
        elif df['High'].iloc[i] >= tp_price :
            profit = tp_price - entry_price
            balance += profit
            trade.append({
                'type' : 'BUY TP', 
                'price' : tp_price,
                'index' : i,
                'profit' : profit
            })
            position = 0

        elif df['Close'].iloc[i] < df['mean'].iloc[i] or df['adx'].iloc[i] <= 15 :
            profit = price - entry_price
            balance += profit
            trade.append({
                'type' : 'BUY EXIT',
                'price' : price,
                'index' : i,
                'profit' : profit
            })
            position = 0

    elif position == -1 :
        sl_price = entry_price + df['standar_deviation'].iloc[i]
        tp_price = entry_price - (2 * df['standar_deviation'].iloc[i])

        if df['High'].iloc[i] >= sl_price :
            profit = entry_price - sl_price
            balance += profit
            trade.append({
                'type' : 'SELL SL', 
                'price' : sl_price,
                'index' :  i,
                'profit' : profit
            })
            position = 0
        
        elif df['Low'].iloc[i] <= tp_price :
            profit = entry_price - tp_price
            balance += profit
            trade.append({
                'type' : 'SELL TP', 
                'price' : tp_price, 
                'index' : i,
                'profit' : profit
            })
            position = 0

        elif df['Close'].iloc[i] >= df['mean'].iloc[i] or df['adx'].iloc[i] <= 15:
            profit = entry_price - price
            balance += profit
            trade.append({
                'type' : 'EXIT SHORT', 
                'price' : price, 
                'index' : i,
                'profit' : profit
            })
            position = 0




# HASIL

print("Initial: ", initial_balance)
print("Final: ", balance)
print("Profit: ", balance - initial_balance)

print("\nHasil dimasukan ke folder outputs/results ")

trade_df = pd.DataFrame(trade)

trade_df = trade_df [
    [
        'type',
        'price',
        'index',
        'profit'
    ]
]

trade_df['price'] = trade_df['price'].round(2)
trade_df['profit'] = trade_df['profit'].round(2)


trade_df.to_csv('../outputs/results/GC=F_1m_backtest.csv', index=False)