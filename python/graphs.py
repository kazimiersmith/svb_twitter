import pandas as pd
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

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

for symbol in ['SVB', 'SBNY', 'FRC']:
    posts_prices_filename = symbol + '_posts_prices.pickle'
    posts_prices = pd.read_pickle(data_out / posts_prices_filename)

    # Note that trading SVB was halted at 8:30am NY time on March 10th

    for i in range(1, 11):
        to_graph = posts_prices[(posts_prices['time'] >= datetime(2023, 3, i)) &
                                     (posts_prices['time'] < datetime(2023, 3, i + 1))]

        # Plot price and number of posts over time, with price and number of posts on two separate y-axes
        figure, ax1 = plt.subplots()

        color = 'tab:red'
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Price (minute level)', color = color)
        ax1.plot(to_graph['time'], to_graph['price'], color = color)
        ax1.tick_params(axis = 'y', labelcolor = color)

        # X axis tick labels every 2 hours, labeled with hour
        ax1.xaxis.set_major_locator(mdates.HourLocator(interval = 2))
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

        # Rotate x axis tick labels
        for tick in ax1.get_xticklabels():
            tick.set_rotation(45)

        ax2 = ax1.twinx()

        color = 'tab:blue'
        ax2.set_ylabel('Cumulative # posts (minute level)', color = color)
        ax2.plot(to_graph['time'], to_graph['cum_num_posts'], color = color)
        ax2.tick_params(axis = 'y', labelcolor = color)

        title = symbol + ' price and Twitter posts on March ' + str(i) + ' 2023'
        ax2.set_title(title)

        figure.tight_layout()
        
        fig_name = symbol + '_price_posts_' + str(i) + '.png'
        plt.savefig(fig / fig_name, dpi = default_dpi)

        # Close the figure to free up memory. Note that plt.clf doesn't free up memory, apparently
        plt.close()
