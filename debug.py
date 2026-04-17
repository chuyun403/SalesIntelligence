import pandas as pd

df = pd.read_csv("data/transactions_clean.csv")
print("Columns in your saved file:")
print(df.columns.tolist())