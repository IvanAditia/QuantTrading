import pandas as pd

from src.data.loader import load_csv

path = load_csv('')

df = pd.read_csv(path)

myvar = pd.DataFrame(data)

print(myvar.loc[[0, 1]])