import os
import json
import subprocess

def extract_time(time_str):
    start_pos = time_str.find("Time: ") + len("Time: ")
    end_pos = time_str.find(" ms")
    return float(time_str[start_pos:end_pos])

filenames = ["1", "2", "3a", "3b", "4a", "4b"]

for filename in filenames:
    with open(f"stack/{filename}.sql") as f:
        queries = f.readlines()
        for qid, query in enumerate(queries):
            results = []
            for i in range(1):
                query = "EXPLAIN ANALYZE " + query
                command = "psql -d stack -c \"" + query + "\""
                # execute the command and fetch the output
                print(f"running query {qid}:\n{query}")
                output = subprocess.check_output(command, shell=True)
                # convert to string
                output = output.decode("utf-8")
                output = output.strip().split("\n")
                plan = output[:-4]
                exec_time_str = output[-2]
                plan_time_str = output[-3]
                exec_time = extract_time(exec_time_str)
                plan_time = extract_time(plan_time_str)
                results.append({
                    "plan_time": plan_time,
                    "exec_time": exec_time,
                    "plan": plan,
                })
            # write the results to a file
            with open(f"results_stack/{filename}-{qid}.jsonl", "a+") as f:
                for result in results:
                    f.write(json.dumps(result) + "\n")