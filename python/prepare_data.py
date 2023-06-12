import pandas as pd
from pathlib import Path
from datetime import datetime
import numpy as np
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

# Identifier for the bank I'm looking at
symbol = 'SBNY'

input_file_list = ['hashtag_sbny.json', 'cashtag_sbny.json']

json_data = []
for file in input_file_list:
    json_data.append(pd.read_json(data_twitter / file, lines = True))

# Combine the two dataframes
posts = pd.concat(json_data, ignore_index = True)

# Drop duplicate ids
posts = posts.drop_duplicates(subset = 'id')

# Read in price data
price_minute_filename = symbol + '_price_minute.dta'
price_minute = pd.read_stata(data_in / price_minute_filename)
price_minute = price_minute.rename(columns = {'tminute': 'time'})

resample_method = 'min'

# Aggregate price data (don't need this, price_minute is already aggregated)
#ctm_agg_methods = {'price': 'mean'}
#ctm_agg = ctm.set_index('tc').resample(resample_method).agg(ctm_agg_methods).reset_index()
#ctm_agg = ctm_agg.rename(columns = {'tc': 'time'})

# Aggregate post data
posts_agg_methods = {'id': 'count'}
posts_agg = posts.set_index('date').resample(resample_method).agg(posts_agg_methods).reset_index()
posts_agg = posts_agg.rename(columns = {'date': 'time', 'id': 'num_posts'})

# Convert Tweet times to New York time and then remove time zone information (we don't really need it)
posts_agg['time'] = posts_agg['time'].dt.tz_convert('America/New_York')
posts_agg['time'] = posts_agg['time'].dt.tz_localize(None)

# Merge posts seconds and ctm_agg
posts_prices = pd.merge(posts_agg, price_minute, on = 'time', how = 'outer')

# Cumulative number of posts
posts_prices['cum_num_posts'] = posts_prices['num_posts'].cumsum()

posts_prices_filename_pickle = symbol + '_posts_prices.pickle'
posts_prices_filename_csv = symbol + '_posts_prices.csv'
posts_prices.to_pickle(data_out / posts_prices_filename_pickle)

# Write to CSV for debugging
posts_prices.to_csv(temp / posts_prices_filename_csv, index = False)
