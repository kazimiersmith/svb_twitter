import pandas as pd
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt

pd.options.display.max_rows = 1000

drive = Path.cwd().drive

if drive == 'E:':
    # Home PC
    root = Path('E:/Dropbox/sivb')
elif drive == 'C:':
    # Work PC
    root = Path('C:/Users/kas1112/Dropbox/sivb')
else:
    # Macbook
    root = Path('/Users/kazimiersmith/Dropbox/sivb')

data = root / 'data'
data_in = data / 'in'
data_out = data / 'out'
data_twitter = data_in / 'twitter'
temp = data / 'temp'
fig = root / 'fig'

default_dpi = 300

posts_ctm_seconds = pd.read_pickle(data_out / 'posts_ctm_seconds.pickle')

# Note that trading was halted at 8:30am NY time on March 10th
to_graph = posts_ctm_seconds[(posts_ctm_seconds['time'] >= datetime(2023, 3, 8, 12)) &
                             (posts_ctm_seconds['time'] <= datetime(2023, 3, 8, 20))]

# Plot price and number of posts over time, with price and number of posts on two separate y-axes
figure, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('Time')
ax1.set_ylabel('Price', color = color)
ax1.plot(to_graph['time'], to_graph['price'], color = color)
ax1.tick_params(axis = 'y', labelcolor = color)

ax2 = ax1.twinx()

color = 'tab:blue'
ax2.set_ylabel('Number of posts', color = color)
ax2.plot(to_graph['time'], to_graph['num_posts'], color = color)
ax2.tick_params(axis = 'y', labelcolor = color)

figure.tight_layout()

plt.savefig(fig / 'price_posts.png', dpi = default_dpi)
plt.clf()

# Write to CSV for debugging
to_graph.to_csv(temp / 'to_graph.csv')
