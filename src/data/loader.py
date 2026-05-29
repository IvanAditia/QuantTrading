from importlib.resources import path
import pandas as pd
from config.paths import DATA_DIR

def load_csv(df):
    path = DATA_DIR / 'XAUUSD_M1.csv'

    df = pd.DataFrame(path)

    