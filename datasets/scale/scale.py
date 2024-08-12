import pandas as pd
import sys
import os
import yaml
from tqdm import tqdm

scale = int(sys.argv[1])

# read tables
original_tables = {
    'badges': pd.read_csv('../stats_simplified/badges.csv'),
    'comments': pd.read_csv('../stats_simplified/comments.csv'),
    'posts': pd.read_csv('../stats_simplified/posts.csv'),
    'users': pd.read_csv('../stats_simplified/users.csv'),
    'votes': pd.read_csv('../stats_simplified/votes.csv'),
    'tags': pd.read_csv('../stats_simplified/tags.csv'),
    'postHistory': pd.read_csv('../stats_simplified/postHistory.csv'),
    'postLinks': pd.read_csv('../stats_simplified/postLinks.csv'),
}

save_path = f"/mydata/stats_scale_{scale}"
os.makedirs(save_path, exist_ok=True)
with open("metadata.yaml") as f:
    metadata = yaml.load(f, Loader=yaml.FullLoader)

for batch_id in range(scale//100):
    new_tables = {
        'badges': pd.DataFrame(),
        'comments': pd.DataFrame(),
        'posts': pd.DataFrame(),
        'users': pd.DataFrame(),
        'votes': pd.DataFrame(),
        'tags': pd.DataFrame(),
        'postHistory': pd.DataFrame(),
        'postLinks': pd.DataFrame(),
    }
    for scale_id in tqdm(range(100)):
        n_scale = scale_id + batch_id * 100
        if scale_id == 0 and batch_id == 0:
            for table in original_tables:
                new_tables[table] = original_tables[table].copy(deep=True)
        else:
            for tablename, table in original_tables.items():
                new_table = table.copy(deep=True)
                for column in table.columns:
                    if metadata[tablename][column] == 'pkey':
                        offset = (table[column].max() + 2) * n_scale
                        new_table[column] += offset
                    elif metadata[tablename][column].startswith('fkey'):
                        fkey_tablename = metadata[tablename][column].split('-')[1]
                        offset = (original_tables[fkey_tablename]['Id'].max() + 2) * n_scale
                        new_table[column] += offset
                    else:
                        assert metadata[tablename][column] == 'data'
                new_tables[tablename] = pd.concat([new_tables[tablename], new_table], ignore_index=True)
    for tablename, table in new_tables.items():
        table.to_csv(f"{save_path}/{tablename}_{batch_id}.csv", index=False)
    print(f"Batch {batch_id} done")
    del new_tables

            
                        