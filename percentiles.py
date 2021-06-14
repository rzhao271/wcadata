# Graphs percentile plots
# DV: best competitor singles/averages for a given event
# IV: percentiles of a given event

import mariadb
import json
import sys
import matplotlib.pyplot as plt
from math import log10

img_dir = "img/percentiles"
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

# Consider events to use
cur = conn.cursor()
event_names_by_id = dict()

events = ['222', '333', '444', '555', '666', '777'] + \
    ['pyram', 'minx', 'skewb', 'sq1'] + \
    ['333oh', '333bf', '444bf', '555bf'] + \
    ['333ft', 'clock']
in_query = "(" + repr(events)[1:-1] + ")"
cur.execute("SELECT id, name from Events WHERE id IN " + in_query)
for (event_id, event_name) in cur:
    event_names_by_id[event_id] = event_name

fig, ax = plt.subplots()
for event_id in events:
    for time_type in ['averages', 'singles']:
        event_name = event_names_by_id[event_id]

        # Get average times from given event
        table = 'RanksAverage' if time_type == 'averages' else 'RanksSingle'
        cur.execute(f"SELECT best from {table} WHERE eventId=?", (event_id,))

        # Convert to list
        times = []
        for (best,) in cur:
            times.append(best / 100)
        percentiles = []
        for i in range(len(times)):
            linear_percentile = (i + 1)/len(times) * 100
            percentile_to_use = linear_percentile
            percentiles.append(percentile_to_use)

        # Make a percentile plot
        ax.scatter(percentiles, times)
        ax.grid(which='both', alpha=0.3)
        ax.set_yscale('log')
        ax.set_xlabel('Top x percentile')
        ax.set_ylabel('Time (seconds)')
        ax.set_title(f'WCA percentiles for {event_name} {time_type}')

        # Save two copies, one loglinear, other loglog
        for graph_type in ['linear', 'log']:
            ax.set_xscale(graph_type)
            figure_file_name = f"percentiles-for-{event_id}-{time_type}-log{graph_type}"
            plt.savefig(f"{img_dir}/{figure_file_name}.png")
        
        plt.cla()
