# n^3 event number of solvers with at least one valid time
# Bar chart
# DV: number of WCA competitors with at least one valid single for id in IV
# IV: puzzle IDs 222 to 777

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
event_counts = dict()
for i in range(2, 8):
    event_id = str(i) * 3
    event_name = f"{i}x{i}x{i}"
    cur.execute("SELECT COUNT(*) from RanksSingle WHERE eventId=?;", (event_id,))
    (num_solvers,), = cur
    event_counts[event_name] = num_solvers

plt.rc('font', size=14)
fig, ax = plt.subplots(figsize=(10, 8))
bars = ax.bar(event_counts.keys(), event_counts.values())
plt.bar_label(bars, labels=event_counts.values())
ax.grid(axis='y', alpha=0.3)

ax.set_xlabel('Event')
ax.set_ylabel('No. of competitors with at least one valid single')
ax.set_title('Number of WCA competitors for nxnxn Events')
plt.savefig(f"{img_dir}/nnn-counts.png", bbox_inches='tight')

