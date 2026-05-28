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

posititon = 0
entry_price = 0
balance = 100


print(df['standar_deviation'])
print(df['mean'])
print(df['adx'])
# KRITERIA CANDLE

df['body'] = abs(df['Close'] - df['Open'])

df['range_body'] = (df['body'] >= 100)  & (df['body'] <= 200)

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
    df['Close'] > df['mean'] &
    df['range_body'] &
    df['upper_wick_range'] &
    df['prev_candle_bull'] &
    df['adx'] >= 21
)

df['sell_entry'] = (
    df['Close'] < df['mean'] & 
    df['range_body'] &
    df['Lower_wick_range'] &
    df['prev_candle_bear'] &
    df['adx'] >= 21
)

# BACKTEST LOOPING

for i in range(df['mean'], len(df)):
    price = df['Close']

    # ENTRY
    if position == 0:
        if df['buy_entry']:
            position = 1
            entry_price = price
            trade.append("BUY", price, i)

        elif df['sell_entry']:
            position = -1
            entry_price = price
            trade.append('SELL', price, i)

        elif df['adx'] <= 20 
            position = 0

    # EXIT, SL, TP
    elif position == 1 :
        sl_price = entry_price - df['standar_deviation']
        tp_price = entry_price + (2 * df['standar_deviation'])

        if df['Low'] <= sl_price  :            
            profit = sl_price - entry_price
            balance += profit
            trade.append("BUY SL", sl_price, i, position = 0)
        elif df['High'] >= tp_price :
            profit = tp_price - entry_price
            balance += profit
            trade.append("BUY TP", tp_price, i, position = 0)

        elif df['Close'] < df['mean'] or df['adx'] <= 20 :
            profit = price - entry_price
            balance += profit
            trade.append("BUY EXIT", price, i, position = 0)

    elif position == -1 :
        sl_price = entry_price + df['adx']
        tp_price = entry_price - (2 * df['adx'])

        if df['High'] >= sl_price :
            profit = entry_price - sl_price
            balance += profit
            trade.append("SELL SL", sl_price, i, position = 0)
        
        elif df['Low'] <= tp_price :
            profit = entry_price - tp_price
            balance += profit
            trade.append("SELL TP", tp_price, i, position = 0)

        elif df['Close'] >= df['mean'] or df['adx'] <= 20:
            profit = entry_price - price
            balance += profit
            trade.append('EXIT SHORT', price, i, position = 0)