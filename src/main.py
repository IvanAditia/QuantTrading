from src.data.download import download
import sys
from src.features.indicator import indicator

from src.data.loader import load_csv

mode = sys.argv[1]

def main(df):

    if mode == 'download':
        download()

    elif mode == 'loader':
        load_csv()

    elif mode == 'indicator':
        indicator(df)

    








