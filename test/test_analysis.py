from email import header
from wsgiref import headers
import pandas as pd
from tabulate import tabulate

import atexit



df = pd.read_csv('../data/XAUUSD_M1.csv')

df = pd.DataFrame(df)

def test(df):
    df['range_candle'] = abs(df['open'] - df['close'])

    # rata-rata candle yang akan bullish
    df['bull_candle'] = df['close'] > df['open']
    df['bull_1'] = df['close'].shift(-1) > df['open'].shift(-1)
    df['bull_2'] = df['close'].shift(-2) > df['open'].shift(-2)
    df['mean_price'] = df['range_candle'].rolling(14).mean()


    df['valid_candle'] = (
        (df['bull_candle']) &
        (df['bull_1']) &
        (df['bull_2'])
    )

    valid_df = df[df['valid_candle']]

    mean = valid_df['range_candle'].mean()


    
    print(mean)
    print(
        tabulate(
            valid_df.head(),
            headers='keys',
            tablefmt='grid'
        )
    )
    print(' jumlah data yang sesuai adalah :', valid_df.sum())
    



    return df 

test(df)