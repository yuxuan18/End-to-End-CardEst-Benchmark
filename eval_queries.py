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

method = sys.argv[1]
os.makedirs(f"results_{method}", exist_ok=True)

with conn.cursor() as cur:
    with open(f"workloads/stats_CEB/stats_CEB.sql") as f:
        lines = f.readlines()
        qid = 1
        for line in lines:
            method_setup = "SET ml_joinest_enabled=true; SET join_est_no=0; SET ml_joinest_fname='stats_CEB_sub_queries_flat.txt';"
            if method != "postgres":
                query = method_setup + "explain analyze " + line.split("||")[1]
            else:
                query = "explain analyze " + line.split("||")[1]
            cur.execute(query)
            result = cur.fetchall()
            plan = [op[0] for op in result[:-2]]
            plan_time = extract_time(result[-2][0])
            exec_time = extract_time(result[-1][0])
            print(plan, plan_time, exec_time)
            result = {
                "plan_time": plan_time,
                "exec_time": exec_time,
                "plan": plan,
            }
            with open(f"results_{method}/{qid}.jsonl", "a+") as f:
                f.write(json.dumps(result) + "\n")
            qid += 1
            

conn.close()