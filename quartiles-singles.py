# Valid best single times for each event
# Horizontal box plot
# Plot different graphs so that it's easier to see the times

import json
import sys

import mariadb
import matplotlib.pyplot as plt
import numpy as np

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

# Get count of single times from all current events
# Leave out FMC and MBLD
event_times = dict()
valid_events = {'222', '333', '444', '555', '666', '777', 
                '333oh', '333bf', '444bf', '555bf',
                'clock', 'minx', 'pyram', 'skewb', 'sq1'}
cur.execute('SELECT eventId, best FROM RanksSingle')

while (row := cur.fetchone()) is not None:
    event_id, best = row
    if event_id in valid_events:
        if event_id not in event_times:
            event_times[event_id] = []
        event_times[event_id].append(best / 100.0)

columns = []
for event_id, times in event_times.items():
    columns.append((event_id, np.array(times, dtype='double')))

# Sort by median
columns.sort(key=lambda entry: np.median(entry[1]))

def plot(columns, tick_step, file_name):
    keys, values = zip(*columns)

    plt.rc('font', size=14)
    fig, ax = plt.subplots(figsize=(12, 10))

    # Don't show the outliers because they stretch the graph too much
    ax.boxplot(values, labels=keys, showfliers=False)
    _, top = ax.get_ylim()
    plt.yticks(np.arange(0, top, step=tick_step))
    ax.grid(axis='y', alpha=0.3)

    ax.set_ylabel('Competitor best single times in seconds')
    ax.set_xlabel('Event')
    ax.set_title('WCA single solve times per event')
    plt.savefig(f"{img_dir}/{file_name}", bbox_inches='tight')
    fig.clear()

plot(columns, 120, 'quartiles-singles.png')

# Now filter out 4BLD and 5BLD
zoom1_columns = [column for column in columns if column[0] not in ['444bf', '555bf']]
plot(zoom1_columns, 30, 'quartiles-singles-zoom1.png')

# Now filter out 4x4x4 and up
allow_list = ['222', 'skewb', 'pyram', 'clock', '333', '333oh', 'sq1']
zoom2_columns = [column for column in columns if column[0] in allow_list]
plot(zoom2_columns, 5, 'quartiles-singles-zoom2.png')
