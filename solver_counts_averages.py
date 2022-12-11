# Number of solvers with at least one valid average
# Horizontal bar chart

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

# Get count of average times from given events
event_counts = dict()
cur.execute("SELECT eventId, COUNT(*) AS counts FROM RanksAverage GROUP BY eventId")

while (row := cur.fetchone()) is not None:
    event_id, num_solvers = row
    event_counts[event_id] = num_solvers

items = list(event_counts.items())
items.sort(key=lambda row: row[1])
x, y = zip(*items)

plt.rc('font', size=14)
fig, ax = plt.subplots(figsize=(12, 10))
bars = ax.barh(x, y)
plt.bar_label(bars, labels=y, padding=1)
ax.grid(axis='x', alpha=0.3)

ax.set_ylabel('Event')
ax.set_xlabel('No. of competitors with at least one valid average')
ax.set_title('Number of WCA competitors with an average per event')
plt.savefig(f"{img_dir}/solver-counts-averages.png", bbox_inches='tight')
