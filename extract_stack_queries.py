import pickle, glob

folders = ["stack/1", "stack/2", "stack/3a", "stack/3b", "stack/4a", "stack/4b"]
for folder in folders:
    query_files = glob.glob(folder + "/*.pkl")
    queries = []
    for query_file in query_files:
        with open(query_file, "rb") as f:
            query = pickle.load(f)["sql"].replace("\n", " ")
            queries.append(query)
    with open(f"{folder}.sql", "w") as f:
        for query in queries:
            f.write(query + "\n")