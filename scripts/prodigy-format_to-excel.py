#!/usr/bin/env python
# coding: utf-8

import json
import pandas as pd
import os

# data in and out names
data_raw = "tpb_tweets_filtered_20220328.json"
data_in = 'tpb_tweets_simple-filter_labelled-prodigy-format_20220408.json'
data_out_n = 'tpb_tweets_labelled.xlsx'

# columns names for labels
#label_cols = ["Physical stuckness and Covid","Pandemic precarity","Blocked and derailed mobilities because of Covid","New mobilities in relation to Covid","Other"]
label_cols = ['blocked mobilities', 'new mobilities', 'pandemic precarity','physical stuckness', 'surrounding precarity and vulnerabilities']

data_d = os.path.join('..', 'data')

# data paths
data_raw_p = os.path.join(data_d, data_raw)
data_in_p = os.path.join(data_d, data_in)
data_out_p = os.path.join(data_d, data_out_n)

# loading data
with open(data_raw_p, 'r') as f:
    data = json.load(f)

df_raw = pd.DataFrame.from_records(data).drop_duplicates('id')

with open(data_in_p, 'r') as f:
    data = json.load(f)

df_in = pd.DataFrame.from_records(data).drop_duplicates(subset = 'id')

# convert labels to dummy variables
df_in = df_in.explode('accept')
df_in['accepted'] = 1
df_in_labeldummies = pd.merge(df_raw, df_in.pivot(index = 'id', columns="accept", values="accepted").reset_index().loc[:, ['id'] + label_cols].fillna(0), how = 'inner', on = 'id')

# reorder columns
columns_neworder = ['created_at', 'name', 'username', 'text', 'tweet_link', 'covid'] + label_cols + ['id', 'hashtags', 'urls', 'retweet_count', 'reply_count',
                                                                                                     'like_count', 'quote_count', 'referenced_type', 'referenced_id']
df_out = df_in_labeldummies.loc[:, columns_neworder]

# export
df_out.to_excel(data_out_p, index = False)