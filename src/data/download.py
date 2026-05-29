from re import S
import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime

from src.config.paths import DATA_DIR


def download():

    # CONNECT MT5
    if not mt5.initialize():

        print("MT5 gagal connect")

        return

    # AMBIL DATA XAUUSD
    rates = mt5.copy_rates_range(
        "XAUUSD.pc",
        mt5.TIMEFRAME_M1,
        datetime(2026, 3, 25),
        datetime(2026, 5, 29)
    )

    print(rates)

    # UBAH KE DATAFRAME
    df = pd.DataFrame(rates)

    # CONVERT TIME

    df['time'] = pd.to_datetime(
        df['time'],
        unit='s'
    )

    # SAVE TO CSV

    df.to_csv(
        DATA_DIR / 'XAUUSD_M1.csv',
        index=False
    )

    print(df.columns)
    print(df.head())
    print(df.tail())
    print(f"\nTOTAL DATA: {len(df)}")

    # CLOSE CONNECTION

    mt5.shutdown()