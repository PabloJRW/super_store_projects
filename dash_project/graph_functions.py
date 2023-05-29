import os
import pandas as pd

DATA_PATH = os.path.join('..','datasets','raw','Superstore.csv')
store_df = pd.read_csv(DATA_PATH, parse_dates=['Order Date', 'Ship Date'], encoding='latin-1')
store_df.set_index('Order Date', inplace=True)
print(store_df)