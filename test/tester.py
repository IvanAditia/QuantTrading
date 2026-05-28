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
    df['Close'] > df['mean'] 
    
)

