import time
from pandas.io.sql import read_sql
import psycopg2
import csv

def wrap_query(query: str, timeout: int):
    query = query[:6] + " ONLINE" + query[6:]
    query += f" WITHTIME {timeout} CONFIDENCE 95 REPORTINTERVAL {timeout};"
    return query

sub_queries = []
qids = []
with open("../workloads/stats_CEB/sub_plan_queries/stats_CEB_sub_queries.sql") as f:
    for line in f:
        sub_queries.append(line.split("||")[0].strip().split(";")[0])
        qids.append(line.split("||")[-1].strip())

timeouts = [7000, 9000]
for timeout in timeouts:
    sub_approx_query = []
    for query in sub_queries:
        approx_query = wrap_query(query, timeout=timeout)
        sub_approx_query.append(approx_query)

    connection = psycopg2.connect("dbname=stats user=yuxuan18 host=/tmp", )

    with open(f"wj_{timeout}.csv", "w") as f:
        f.write("qid,timeout,n_sample,n_reject,estimate,rel_ci,runtime\n")

    results = []
    assert len(sub_approx_query) == len(qids)
    for approx_query, qid in zip(sub_approx_query, qids):
        start = time.time()
        try:
            result = [qid] + read_sql(approx_query, connection).iloc[0].to_list()
        except Exception as e:
            print(e)
            result = [qid, None, None, None, None, None]
        runtime = time.time() - start
        result.append(runtime)
        with open(f"wj_{timeout}.csv", "a+") as f:
            writer = csv.writer(f)
            writer.writerow(result)
