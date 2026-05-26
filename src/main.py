from unittest import result
from src.data.loader import load_csv
from src.analysis.momentum import analyze_momentum

def main():
    df = load_csv("data/raw/GC=F_5m.csv")

    result = analyze_momentum(df)

    print(result.head())