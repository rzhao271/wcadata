# Graphs scatterplots
# DV: number of WCA competitors with 
# average bucket for a given event

import mariadb
import json
import sys
import matplotlib.pyplot as plt

event = "pyram"
timecap = 20
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

# Get average times from given event
cur = conn.cursor()
cur.execute("SELECT best from RanksAverage WHERE eventId=?",
(event,))

# Convert to list
times = []
for (best,) in cur:
    times.append(best / 100) 

# Make a histogram
timecount = dict()
for time in times:
    if int(time) > timecap:
        break
    if int(time) not in timecount:
        timecount[int(time)] = 0
    timecount[int(time)] += 1

fig, ax = plt.subplots()
ax.scatter(timecount.keys(), timecount.values())
ax.set_xlabel('Time (floor(seconds))')
ax.set_ylabel('No. of Solvers')
ax.set_title('WCA averages for event ' + event)
plt.savefig(f"{img_dir}/averages-for-{event}.png")

