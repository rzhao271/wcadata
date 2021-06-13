# n^3 event averages
# Graphs scatterplots
# DV: number of WCA competitors with average IV for all puzzles 222 to 777
# IV: floor(seconds)

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

# Get average times from given events
event_times = dict()
timecap = 300
for i in range(2, 8):
    event_id = f"{i}" * 3
    event_name = f"{i}x{i}x{i}"
    cur.execute("SELECT best from RanksAverage WHERE eventId=?", (event_id,))

    # Convert to list
    times = []
    for (best,) in cur:
        avg_in_seconds = best / 100
        if avg_in_seconds > timecap:
            break
        times.append(avg_in_seconds) 

    # Make a histogram
    timecount = dict()
    for time in times:
        if int(time) not in timecount:
            timecount[int(time)] = 0
        timecount[int(time)] += 1
    event_times[event_name] = timecount

fig, ax = plt.subplots()
for event_name, timecount in event_times.items():
    ax.scatter(timecount.keys(), timecount.values(), label=event_name)

ax.legend()
ax.set_xlabel('Time (floor(seconds))')
ax.set_ylabel('No. of Solvers')
ax.set_title('WCA averages for nxnxn events')
plt.savefig(f"{img_dir}/nnn-averages.png")

