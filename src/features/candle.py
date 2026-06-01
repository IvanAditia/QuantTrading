
def candle(df):

    # CANDLE
    # =======
    
    df['body'] = abs(df['close'] - df['open'])
    df['upper_wick'] = df['high'] - df[['open', 'close']].max(axis=1)
    df['lower_wick'] = df[['open', 'close']].min(axis=1) - df['low']

    # KRITERIA CANDLE
    df['bull_candle'] = df['close'] > df['open']
    df['bear_candle'] = df['close'] < df['open']
    df['bull_1'] = df['close'].shift(-1) > df['open'].shift(-1)
    df['bull_2'] = df['close'].shift(-2) > df['open'].shift(-2)
    df['bear_1'] = df['close'].shift(-1) < df['open'].shift(-1)
    df['bear_2'] = df['close'].shift(-2) < df['open'].shift(-2)


    return df

