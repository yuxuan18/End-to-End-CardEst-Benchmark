import sys
import glob
from tqdm import tqdm
import pandas as pd

data_path = sys.argv[1]
data_files = glob.glob(f"{data_path}/*.csv")

for data_file in tqdm(data_files):
    df = pd.read_csv(data_file)
    for column in df.columns:
        if 'id' in column.lower() or 'count' in column.lower() or 'amount' in column.lower():
            # cast non-na values to int
            df[column] = df[column].fillna(-100).astype(int)
            # cast -100 to NaN
            df[column] = df[column].replace(-100, pd.NA)
    df.to_csv(data_file, index=False)
