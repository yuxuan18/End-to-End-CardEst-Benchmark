import csv
import sys
timeout = sys.argv[1]

queries_to_run = set()

lines = []

with open(f"wj_{timeout}.csv") as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        if row[1] != "" and int(float(row[4])) != 0:
            queries_to_run.add(row[0])
            lines.append(row[4])
        else:
            lines.append("-1")

with open(f"wj_{timeout}.txt", "w") as f:
    for line in lines:
        f.write(line + "\n")