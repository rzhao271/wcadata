# smol events number of solvers with at least one valid time
# Bar chart
# DV: number of WCA competitors with at least one valid single for id in IV
# IV: puzzle IDs minx, clock, pyram, skewb, sq1, 222, 333

import mariadb
import json
import sys
import matplotlib.pyplot as plt

img_dir = "img"
creds_dir = "creds"

with open(f"{creds_dir}/creds.txt", "r") as f:
    jsons = json.loads(f.read())
    user = jsons["user"]
    password = jsons["password"]

# Connect to DB
try:
    conn = mariadb.connect(
        user=user,
        password=password,
        host="localhost",
        port=3306,
        database="wcadata"
    )
except mariadb.Error as e:
    print(f"Error connecting to mariadb: {e}")
    sys.exit(1)

cur = conn.cursor()

# Get count of single times from given events
event_ids = ["222", "pyram", "skewb", "minx", "sq1", "clock"]
event_counts = dict()
for event_id in event_ids:
    cur.execute("SELECT name from Events WHERE id=?;", (event_id,))
    (event_name,), = cur
    cur.execute("SELECT COUNT(*) from RanksSingle WHERE eventId=?;", (event_id,))
    (num_solvers,), = cur
    event_counts[event_name] = num_solvers

fig, ax = plt.subplots(figsize=(9.6, 4.8))
ax.bar(event_counts.keys(), event_counts.values(), width=0.75)
ax.grid(axis='y', alpha=0.3)

ax.set_xlabel('Event')
ax.set_ylabel('No. of competitors with at least one valid single')
ax.set_title('Number of WCA competitors')
ax.set_aspect('auto')
plt.savefig(f"{img_dir}/smol-counts.png", bbox_inches='tight')

