#!/usr/bin/env python
# coding: utf-8

# Import packages
import json
import os

data_dir = os.path.join('..', 'data')
data_p = os.path.join(data_dir, 'tpb_tweets_filtered_20220328.json')
out_tagset_covid = os.path.join(data_dir, 'prodigy', 'tpb_tagset_covid01.json')
out_tagset_other = os.path.join(data_dir, 'prodigy', 'tpb_tagset_other01.json')

# load data
with open(data_p, "r") as f:
    all_data = json.load(f)
    
# covid set
covid_tweets = [entry for entry in all_data if entry.get('covid') is True and entry.get('referenced_type') is None]

# non-covid set
other_tweets = [entry for entry in all_data if entry.get('covid') is False and entry.get('referenced_type') is None]

# export to prodigy-format
export_keys = ['id', 'username', 'text', 'tweet_link']

covid_out = [{export_key: entry.get(export_key) for export_key in export_keys} for entry in covid_tweets]
other_out = [{export_key: entry.get(export_key) for export_key in export_keys} for entry in other_tweets]

json.dump(covid_out, open(out_tagset_covid, 'w'))
json.dump(other_out, open(out_tagset_other, 'w'))