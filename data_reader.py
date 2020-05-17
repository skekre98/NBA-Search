import pandas as pd

df = pd.read_csv("data/query.csv")
df.columns = ['Query', 'Class']

print("NBA Questions:", (df.Class == 1.0).sum())
print("Random Questions:", (df.Class == 0.0).sum())
