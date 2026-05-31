import MetaTrader5 as mt5
import pandas as pd
from tabulate  import tabulate

df = pd.read_csv('../data/XAUUSD_M1.csv')


print(symbol.trade_contract_size)

def test(df):

    # CANDLE
    # ======

    df['body'] = abs(df['close'] - df['open'])
    df['upper_wick'] = df['high'] - df[['close', 'open']].max(axis=1)
    df['lower_wick'] = df[['open', 'close']].min(axis=1) - df['low']

    # KRITERIA
    # ========

    df['bull_candle'] = df['close'] > df['open']
    df['bear_candle'] = df['close'] < df['open']
    df['bull_1'] = df['close'].shift(-1) > df['open'].shift(-1)
    df['bull_2'] = df['close'].shift(-2) > df['open'].shift(-2)
    df['bear_1'] = df['close'].shift(-1) < df['open'].shift(-1)
    df['bear_2'] = df['close'].shift(-2) < df['open'].shift(-2)

    # INDIKATOR
    # =========

    df['mean'] = df['close'].rolling(14).mean()
    df['sd'] = df['close'].rolling(14).std()

    # CANDLE VALID
    # ============

    df['bull_valid'] = (
        (df['bull_candle']) &
        (df['close'] > df['mean']) &
        (df['bull_1'])  & 
        (df['bull_2'])
    )

    df['bear_valid'] = (
        (df['bear_candle']) & 
        (df['close'] < df['mean']) &
        (df['bear_1']) &
        (df['bear_2'])
    )

    result = df[
        df['bull_valid'] |
        df['bear_valid']
    ]

    result = result[
        ['high', 'open', 'close', 'low']
    ]

    lot = {''}
    return


test(df)