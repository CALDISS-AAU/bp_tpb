#!/usr/bin/env python
# coding: utf-8

import json
import pandas as pd
import os
import re

# data in and out names
data_raw = "tpb_tweets_filtered_20220328.json"
data_in = 'tpb_covidcat_labelled_20220429.jsonl'
data_out_n = 'tpb_covid-tweets_labelled.xlsx'

# columns names for labels
old_label_cols = ['Physical stuckness and Covid', 'Pandemic precarity', 'Blocked and derailed mobilities because of Covid', 'New mobilities in relation to Covid', 'Other']
new_label_cols = ['Physical stuckness and Covid', 'Pandemic precarity', 'Blocked and derailed mobilities in relation to Covid', 'Mobility in relation to Covid ', 'Other']

label_rename_map = dict(zip(old_label_cols, new_label_cols))

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
    data = [json.loads(line) for line in f]

df_in = pd.DataFrame.from_records(data)

id_regex = re.compile(r'(?<=/)(\d{15,20})$')
df_in['id'] = df_in['tweet_link'].str.extract(regex).astype('int')

# tidy - one row per label
df_in = df_in.explode('accept').reset_index(drop = True)
df_in['accept'] = df_in['accept'].replace(label_rename_map)
df_merged = pd.merge(df_in.loc[:, ['id', 'accept']], df_raw, how = 'inner', on = 'id')

# convert labels to dummy variables
#df_in['accepted'] = 1
#df_in_labeldummies = pd.merge(df_raw, df_in.pivot(index = 'id', columns="accept", values="accepted").reset_index().loc[:, ['id'] + label_cols].fillna(0), how = 'inner', on = 'id')

# reorder columns - dummies
#columns_neworder = ['created_at', 'name', 'username', 'text', 'tweet_link', 'covid'] + label_cols + ['id', 'hashtags', 'urls', 'retweet_count', 'reply_count', 'like_count', 'quote_count', 'referenced_type', 'referenced_id']
#df_out = df_in_labeldummies.loc[:, columns_neworder]

# reorder columns - tidy
columns_neworder = ['created_at', 'name', 'username', 'text', 'tweet_link', 'covid', 'accept', 'id', 'hashtags', 'urls', 'retweet_count', 'reply_count', 'like_count', 'quote_count', 'referenced_type', 'referenced_id']
df_out = df_merged.loc[:, columns_neworder].rename(columns = {'accept': 'label'})

# drop ignored (label na)
df_out = df_out.dropna(subset = ['label'])

# id as string
df_out['id'] = df_out['id'].astype('str')

# convert to datetime
df_out['created_at'] = pd.to_datetime(df_out['created_at']).dt.tz_localize(None) # removing timezone

# sort by datetime (old to new)
df_out = df_out.sort_values('created_at')

# export
df_out.to_excel(data_out_p, index = False)