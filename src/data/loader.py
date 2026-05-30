import pandas as pd
from src.config.paths import DATA_DIR
from src.data.cleaner import clean_data

def load_csv():
    path = pd.read_csv(DATA_DIR / 'XAUUSD_M1.csv')

    df = pd.DataFrame(path)

    df = clean_data(df)

    return df