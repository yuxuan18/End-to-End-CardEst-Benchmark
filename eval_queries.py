import sys
import os
import psycopg2
import json

def extract_time(time_str):
    start_pos = time_str.find("Time: ") + len("Time: ")
    end_pos = time_str.find(" ms")
    return float(time_str[start_pos:end_pos])

# Connect to the database
conn = psycopg2.connect("dbname=stats user=postgres password=postgres host=localhost")

with open(f"workloads/stats_CEB/stats_CEB.sql") as f:
    lines = f.readlines()
    for qid, line in enumerate(lines):
        for i in range(1):
            setup2 = f"SET query_no={qid}; SET ml_cardest_enabled=true; SET ml_cardest_fname='stats_CEB_single_table_sub_query_gt.txt'; " + \
                     f"SET join_est_no={qid}; SET ml_joinest_enabled=true; SET ml_joinest_fname='stats_CEB_sub_queries_flat.txt';"
            setup1 = f"SET ml_cardest_enabled=false;SET join_est_no={qid}; SET ml_joinest_enabled=true; SET ml_joinest_fname='stats_CEB_sub_queries_flat.txt';"
            flat_query = setup1 + "explain analyze " + line.split("||")[1]
            with conn.cursor() as cur:
                cur.execute(flat_query)
                result = cur.fetchall()
            plan = [op[0] for op in result[:-2]]
            plan_time = extract_time(result[-2][0])
            exec_time = extract_time(result[-1][0])
            result = {
                "plan_time": plan_time,
                "exec_time": exec_time,
                "plan": plan,
            }
            with open(f"results_flat/{qid}.jsonl", "a+") as f:
                f.write(json.dumps(result) + "\n")
            print(result)

            postgres_query = "SET ml_cardest_enabled=false; SET ml_joinest_enabled=false;" + "explain analyze " + line.split("||")[1]
            with conn.cursor() as cur:
                cur.execute(postgres_query)
                result = cur.fetchall()
            plan = [op[0] for op in result[:-2]]
            plan_time = extract_time(result[-2][0])
            exec_time = extract_time(result[-1][0])
            result = {
                "plan_time": plan_time,
                "exec_time": exec_time,
                "plan": plan,
            }
            with open(f"results_postgres/{qid}.jsonl", "a+") as f:
                f.write(json.dumps(result) + "\n")
            print(result)

conn.close()