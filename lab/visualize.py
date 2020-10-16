import pandas as pd
from data.text_data import total_stat_map, adv_stat_map

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
    print("Ranking Questions:", (df.Class == "rank").sum())
    print("Stat Questions:", (df.Class == "stat").sum())

def read_stat_maps():
    print("Total:", total_stat_map)
    print()
    print("Advanced:", adv_stat_map)

def main():

    print("Reading query dataset...")
    read_query_csv()
    print()
    print("Reading stat maps...")
    read_stat_maps()

if __name__ == "__main__":
    main()