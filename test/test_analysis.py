import pandas as pd
from tabulate  import tabulate
import ta
import matplotlib.pyplot as plt


df = pd.read_csv('../data/XAUUSD_M1.csv')

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
    df['adx'] = ta.trend.ADXIndicator(
        high=df['high'],
        low=df['low'],
        close=df['close'],
        window=14
    ).adx()

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
        ['high', 'open', 'close', 'low', 'body']
    ]

    position = 0
    initial_balance = 100
    lot = 0.1
    contract_size = 1
    balance = initial_balance
    trade = []

    df['range_body'] = result['body'].mean()

    print(df['range_body'])


    df['buy_entry'] = (
        (df['bull_valid']) &
        (df['range_body'])
    )

    df['sell_entry'] = (
        (df['bear_valid']) &
        (df['range_body'])
    )
    # BACKTEST
    # ========

    for i in range(14, len(df)):
        price = df['close'].iloc[i]


        # ENTRY
        # ======

        if position == 0:
            if df['buy_entry'].iloc[i]:
                position = 1
                entry_price = price
                trade.append({
                    'type': "BUY",
                    'price': price,
                    'index': i
                })

            if df['sell_entry'].iloc[i]:
                position = -1
                entry_price = price
                trade.append({
                    'type': 'SELL',
                    'price': price,
                    'index': i
                })
            
            if df['adx'].iloc[i] <= 15:
                position = 0

        elif position == 1:
            sl_price = entry_price - df['sd'].iloc[i]
            tp_price = entry_price + (df['sd'].iloc[i] * 2)

            if df['low'].iloc[i] <= sl_price:
                profit = (sl_price - entry_price) * contract_size * lot
                balance += profit
                trade.append({
                    'type' : 'BUY SL',
                    'price' : sl_price,
                    'index' : i,
                    'profit' : profit
                }) 
                position = 0

            elif df['high'].iloc[i] >= tp_price :
                profit = (tp_price - entry_price) * contract_size * lot
                balance += profit
                trade.append({
                    'type' : 'BUY TP',
                    'price' : tp_price,
                    'index' : i,
                    'profit' : profit
                })
                position = 0

            elif df['adx'].iloc[i] <= 15 or df['close'].iloc[i] < df['mean'].iloc[i] :
                profit = (price - entry_price) * contract_size * lot
                balance += profit
                trade.append({
                    'type' : 'BUY EXIT',
                    'price' : price ,
                    'index' : i,
                    'profit' : profit
                })
                position = 0


        elif position == -1:
            sl_price = entry_price + df['sd'].iloc[i]
            tp_price = entry_price - (df['sd'].iloc[i] * 2)

            if df['high'].iloc[i] >= sl_price:
                profit = (entry_price - sl_price) * contract_size * lot
                balance += profit
                trade.append({
                    'type': 'SELL SL',
                    'price': sl_price,
                    'index': i,
                    'profit': profit
                })
                position = 0

            elif df['low'].iloc[i] <= tp_price:
                profit = (entry_price - tp_price) * contract_size * lot
                balance += profit
                trade.append({
                    'type': 'SELL TP',
                    'price' : tp_price,
                    'index' : i,
                    'profit': profit
                })
                position = 0

            elif df['adx'].iloc[i] <= 15 or df['close'].iloc[i] > df['mean'].iloc[i]:
                profit = (entry_price - price) * contract_size * lot
                balance += profit
                trade.append({
                    'type' : 'SELL EXIT',
                    'price' : price,
                    'index' : i,
                    'profit': profit
                })
                position = 0


    # HASIL
    # =======
    trade_df = pd.DataFrame(trade)

    trade_df = trade_df[
        [
            'type',
            'price',
            'index',
            'profit'
        ]
    ]

    buy_tp = trade_df['type'].isin( 
        ['BUY TP']
    ).sum()

    buy_profit = trade_df.loc[
        trade_df['type'].isin(
            ['BUY TP']
        ),'profit'
    ].sum()

    buy_sl = trade_df['type'].isin( 
        ['BUY SL']
    ).sum()

    buy_rugi = trade_df.loc[
        trade_df['type'].isin(
            ['BUY SL']
        ),'profit'
    ].sum()

    sell_tp = trade_df['type'].isin( 
        ['SELL TP']
    ).sum()

    sell_profit = trade_df.loc[
        trade_df['type'].isin(
            ['SELL TP']
        ),'profit'
    ].sum()

    sell_sl = trade_df['type'].isin( 
        ['SELL SL']
    ).sum()

    sell_rugi = trade_df.loc[
        trade_df['type'].isin(
            ['SELL SL']
        ),'profit'
    ].sum()

    buy_exit = trade_df['type'].isin( 
        ['BUY EXIT']
    ).sum()

    exit_buy_profit = trade_df.loc[
        trade_df['type'].isin(
            ['BUY EXIT']
        ),'profit'
    ].sum()

    sell_exit = trade_df['type'].isin( 
        ['SELL EXIT']
    ).sum()

    exit_sell_profit = trade_df.loc[
        trade_df['type'].isin(
            ['SELL EXIT']
        ),'profit'
    ].sum()

    total_trade = buy_tp + buy_sl + sell_tp + sell_sl + buy_exit + sell_exit
    total_profit = buy_profit + buy_rugi + sell_profit + sell_rugi + exit_buy_profit + exit_sell_profit
    exit_win = len(trade_df[
        (
            trade_df['type'].isin(
                ['BUY EXIT', 'SELL EXIT']
            ) 
        ) & (
           trade_df['profit'] > 0 
        )
    ])
    total_win = buy_tp + sell_tp + exit_win
    winrate = (total_win/total_trade) * 100
    max_win = trade_df['profit'].max()
    max_loss = trade_df['profit'].min()


    saldo =  [
        {'TYPE':'SALDO AWAL ', 'JUMLAH':    initial_balance },
        {'TYPE':'SALDO AKHIR', 'JUMLAH': balance},
        {'TYPE':'PROFIT', 'JUMLAH': balance - initial_balance}
    ]  

    itrade =[
        {'TYPE': 'BUY TP', 'TOTAL TRADE':buy_tp, 'PROFIT':buy_profit },
        {'TYPE': 'BUY SL', 'TOTAL TRADE':buy_sl, 'PROFIT':buy_rugi },
        {'TYPE': 'SELL TP', 'TOTAL TRADE':sell_tp, 'PROFIT':sell_profit },
        {'TYPE': 'SELL SL', 'TOTAL TRADE':sell_sl, 'PROFIT':sell_rugi },
        {'TYPE': 'EXIT BUY', 'TOTAL TRADE':buy_exit, 'PROFIT':exit_buy_profit},
        {'TYPE': 'EXIT SELL', 'TOTAL TRADE':sell_exit, 'PROFIT':exit_sell_profit},
        {'TYPE': 'TOTAL', 'TOTAL TRADE':total_trade, 'PROFIT': total_profit}
    ]

    trade_df['time'] = df.loc[
            trade_df['index'],
            'time'
    ].values

    trade_df['time'] = pd.to_datetime(
        trade_df['time']
    )

    close_trade = trade_df[
        trade_df['type'].isin([
            'BUY EXIT', \
            'SELL EXIT',
            'BUY TP',
            'SELL TP',
            'BUY SL',
            'SELL SL'
        ])
    ].copy()

    daily_profit = (
        close_trade
        .groupby(
            close_trade['time'].dt.date
        )['profit']
        .sum()
    )

    daily_balance = (
        daily_profit.cumsum()
        + initial_balance        
    )

    print('\nINFORMASI SALDO:')
    print(
        tabulate(
            saldo,
            headers='keys',
            tablefmt='grid'
        )
    )

    print('\nINFORMASI TRADE:')
    print(
        tabulate(
            itrade,
            headers='keys',
            tablefmt='grid'
        )
    )

    print(f'WIN TERTINGGI: {max_win.round(2)}')
    print(f'LOSS TERTINGGI: {max_loss.round(2)}')
    print(f'WINRATE: {winrate.round()}%')

    plt.figure(figsize=(15, 6))
    plt.plot(
        daily_balance.index,
        daily_balance.values
    )
    plt.title('Balance Growth per Day')
    plt.xlabel('tanggal')
    plt.ylabel('balance')

    plt.grid(True)

    plt.show()

    trade_df.to_excel('../outputs/results/gold_m1_backtest.xlsx')

    return


test(df)