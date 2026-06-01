from tabulate import tabulate
import ta

def indicator(df):

    df['mean'] =  df['close'].rolling(14).mean()

    df['sd'] = df['close'].rolling(14).std()

    df['adx'] = ta.trend.ADXIndicator(
        high = df['high'],
        low = df['low'],
        close = df['close'],
        window = 14
    ).adx()
        
    return df