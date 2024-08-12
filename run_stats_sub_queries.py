import psycopg2

# Open a cursor to perform database operations
with open("workloads/stats_CEB/sub_plan_queries/stats_CEB_sub_queries.sql") as f:
    lines = f.readlines()
    for qid, line in enumerate(lines):
        if qid < 589:
            continue
        query = line.split("||")[0]
        conn = psycopg2.connect("dbname=postgres user=yuxuan18")
        with conn.cursor() as cur:
            cur.execute(query)
            result = cur.fetchall()[0][0]
        conn.close()
        with open("workloads/stats_CEB/sub_plan_queries/stats_CEB_sub_queries_gt.txt", "a+") as f:
            f.write(str(result) + "\n")
