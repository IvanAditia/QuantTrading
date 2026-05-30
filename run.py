from src.data.loader import load_csv
from src.main import main

df = load_csv()

main(df)