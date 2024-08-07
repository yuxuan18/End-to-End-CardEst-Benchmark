import psycopg2
from tqdm import tqdm
# Connect to the database
conn = psycopg2.connect("dbname=stats user=postgres password=postgres host=localhost")

# Open a cursor to perform database operations
with conn.cursor() as cur:
    with open("workloads/stats_CEB/sub_plan_queries/stats_CEB_sub_queries.sql") as f:
        lines = f.readlines()
        for line in tqdm(lines):
            query = line.split("||")[0]
            cur.execute(query)
            result = cur.fetchall()[0][0]
            with open("workloads/stats_CEB/sub_plan_queries/stats_CEB_sub_queries_gt.txt", "a+") as f:
                f.write(str(result) + "\n")
