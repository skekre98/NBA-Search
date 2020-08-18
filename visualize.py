import pandas as pd

"""
Function to print query dataset

Parameters
----------
n/a

Returns
-------
n/a
"""
def read_query_csv():
    df = pd.read_csv("data/query.csv")
    df.columns = ['Query', 'Class']
    print("Ranking Questions:", (df.Class == 1.0).sum())
    print("Stat Questions:", (df.Class == 2.0).sum())

def main():

    print()
    print("Reading query dataset...")
    read_query_csv()

if __name__ == "__main__":
    main()