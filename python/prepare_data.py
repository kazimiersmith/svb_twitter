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

# For now, just read in the results from searching #svb, since reading all the data would be slow
posts = pd.read_json(data_twitter / 'hashtag_svb.json', lines = True, encoding = 'utf-16')

# Read in Stata files
bjzz = pd.read_stata(data_in / 'bjzz.dta')
ctm = pd.read_stata(data_in / 'ctm.dta')
price_minute = pd.read_stata(data_in / 'price_minute.dta')

# Aggregate data
resample_method = 'min'
ctm_seconds_agg_methods = {'price': 'mean'}
ctm_seconds = ctm.set_index('tc').resample(resample_method).agg(ctm_seconds_agg_methods).reset_index()
ctm_seconds = ctm_seconds.rename(columns = {'tc': 'time'})

posts_seconds_agg_methods = {'id': 'count'}
posts_seconds = posts.set_index('date').resample(resample_method).agg(posts_seconds_agg_methods).reset_index()
posts_seconds = posts_seconds.rename(columns = {'date': 'time', 'id': 'num_posts'})

# Convert Tweet times to New York time and then remove time zone information (we don't really need it)
posts_seconds['time'] = posts_seconds['time'].dt.tz_convert('America/New_York')
posts_seconds['time'] = posts_seconds['time'].dt.tz_localize(None)

# Merge posts seconds and ctm_seconds
posts_ctm_seconds = pd.merge(posts_seconds, ctm_seconds, on = 'time', how = 'outer')

posts_ctm_seconds.to_pickle(data_out / 'posts_ctm_seconds.pickle')

# Write to CSV for debugging
posts_ctm_seconds.to_csv(temp / 'posts_ctm_seconds.csv')
