import pandas as pd
import yfinance as yf

df = yf.download("GC=F", interval="1m", period="7d")

print(df.tail())

df.to_csv("../data/raw/GC=F_1m.csv")

