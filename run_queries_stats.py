import os
import json
import subprocess

def extract_time(time_str):
    start_pos = time_str.find("Time: ") + len("Time: ")
    end_pos = time_str.find(" ms")
    return float(time_str[start_pos:end_pos])

with open("workloads/stats_CEB/stats_CEB.sql") as f:
    qid = 1
    for line in f:
        results = []
        for i in range(6):
            query = "EXPLAIN ANALYZE " + line.split("||")[1]
            command = "psql -d postgres -c \"" + query + "\""
            # execute the command and fetch the output
            output = subprocess.check_output(command, shell=True)
            if i == 0:
                continue
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
        with open(f"results/{qid}.jsonl", "a+") as f:
            for result in results:
                f.write(json.dumps(result) + "\n")
        qid += 1
