import psycopg2
import os
import time
import random
import argparse

methods = [
    "wj_1000",
    "wj_3000",
    "wj_5000",
    "stats_CEB_single_table_sub_query_gt",
    "stats_CEB_sub_queries_deepdb",
    "stats_CEB_sub_queries_gt",
    "stats_CEB_sub_queries_bayescard",
    "stats_CEB_sub_queries_flat",
    "stats_CEB_sub_queries_neurocard",
]

runid = int(time.time())

def reconstruct_db(conn):
    with conn.cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS users;")
        cursor.execute("DROP TABLE IF EXISTS posts;")
        cursor.execute("DROP TABLE IF EXISTS postLinks;")
        cursor.execute("DROP TABLE IF EXISTS postHistory;")
        cursor.execute("DROP TABLE IF EXISTS comments;")
        cursor.execute("DROP TABLE IF EXISTS votes;")
        cursor.execute("DROP TABLE IF EXISTS badges;")
        cursor.execute("DROP TABLE IF EXISTS tags;")
        conn.commit()
        
        with open("stats.sql") as f:
            queries = f.read().split(";")
            for query in queries:
                if query.strip() == "":
                    continue
                cursor.execute(query.strip())
        conn.commit()
        
        with open("insert_data.sql") as f:
            queries = f.read().split(";")
            for query in queries:
                if query.strip() == "":
                    continue
                cursor.execute(query.strip())
        conn.commit()
        
        with open("stats_index.sql") as f:
            queries = f.read().split(";")
            for query in queries:
                if query.strip() == "":
                    continue
                cursor.execute(query.strip())
        conn.commit()

def run_all(method, conn, mode):
    if not os.path.exists(f"logs/{mode}-{method}-{runid}"):
        os.makedirs(f"logs/{mode}-{method}-{runid}", exist_ok=True)
    with conn.cursor() as cursor:
        cursor.execute("SET ml_cardest_enabled=true;")
        cursor.execute("SET ml_joinest_enabled=true;")
        cursor.execute("SET query_no=0;")
        cursor.execute("SET join_est_no=0;")
        cursor.execute("SET ml_cardest_fname='stats_CEB_single_table_sub_query_gt.txt';")
        cursor.execute(f"SET ml_joinest_fname='{method}.txt';")
        with open("stats_CEB.sql") as f:
            qid = 0
            for line in f:
                query = line.strip().split("||")[-1]
                start = time.time()
                if mode == "explain":
                    cursor.execute("EXPLAIN " + query)
                elif mode == "explain_analyze":
                    cursor.execute("EXPLAIN ANALYZE " + query)
                else:
                    cursor.execute(query)
                output = cursor.fetchall()
                end = time.time()
                if mode != "explain":
                    with open(f"results/{mode}-{method}-{runid}.csv", "a+") as f:
                        f.write(f"{qid},{end - start}\n")
                with open(f"logs/{mode}-{method}-{runid}/{qid}.txt", "w") as f:
                    for line in output:
                        for item in line:
                            f.write(str(item))
                        f.write("\n")
                qid += 1
        cursor.execute("SET ml_cardest_enabled=false;")
        cursor.execute("SET ml_joinest_enabled=false;")
        cursor.execute("SET query_no=0;")
        cursor.execute("SET join_est_no=0;")
        cursor.execute("SET ml_cardest_fname='';")
        cursor.execute("SET ml_joinest_fname='';")
        
def run_all_methods(conn, mode):
    random.shuffle(methods)
    for method in methods:
        run_all(method, conn, mode)


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--host", type=str, default="localhost")
    arg_parser.add_argument("--port", type=int, default=5432)
    arg_parser.add_argument("--user", type=str, default="postgres")
    arg_parser.add_argument("--password", type=str, default="postgres")
    arg_parser.add_argument("--database", type=str, default="stats")
    arg_parser.add_argument("--method", type=str, default="stats_CEB_sub_queries_gt")
    arg_parser.add_argument("--mode", type=str, default="explain")
    args = arg_parser.parse_args()
    try:
        conn = psycopg2.connect(
            host=args.host,
            port=args.port,
            user=args.user,
            password=args.password,
            database=args.database,
        )
    except Exception as e:
        conn = psycopg2.connect(
            host=args.host,
            port=args.port,
            user=args.user,
            password=args.password
        )
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE {args.database}")
        conn.close()
        conn = psycopg2.connect(
            host=args.host,
            port=args.port,
            user=args.user,
            password=args.password,
            database=args.database,
        )
    reconstruct_db(conn)
    if args.method == "all":
        run_all_methods(conn, args.mode)
    else:
        run_all(args.method, conn, args.mode)
    conn.close()

