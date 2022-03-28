#!/usr/bin/env python
# coding: utf-8

# Import packages
import pandas as pd
import ast 
import numpy as np
import json
import re
import os

data_dir = os.path.join('..', 'data')
rawdata_p = os.path.join(data_dir, 'tpb_tweets_news-outlets_20211208.json')
labelled_p = os.path.join(data_dir, 'tpb_tweets_simple-filter_labelled_20220308.json')
out_excel = os.path.join(data_dir, 'tpb_tweets_filtered_20220328.xlsx')
out_tagset = os.path.join(data_dir, 'prodigy', 'tpb_tagset01.json')

keep_columns = ['created_at', 'name', 'username', 'text', 'tweet_link', 'covid', 'label', 'id', 'hashtags', 'urls', 'retweet_count', 
                'reply_count', 'like_count', 'quote_count', 'referenced_type', 'referenced_id']


# load data
with open(rawdata_p, "r") as f:
    all_data = json.load(f)
    
labelled_df = pd.read_json(labelled_p)


# regex strings
regex_string_covid = r'\bpandemic\b|\bcovid\b|\bcovid-19\b|\bcorona|\bvaccine|\bquarantine|\b#pandemic\b|\b#covid\b|\b#covid-19\b|\b#corona|\b#vaccine|\b#quarantine'
regex_string_migrat = r'\bmigrant|\bimmigrant|\brefugee|\btransit|\bdisplacement\b|\bdisplaced\b|\bborder|\breturn|\bpushback|\b(pushed back)\b|\bboat|\bdrown\b|\bhunger|\b#migrant|\b#immigrant|\b#refugee|\b#transit|\b#displacement\b|\b#displaced\b|\b#border|\b#return|\b#pushback|\b#boat|\b#drown\b|\b#hunger'
regex_string_geos = r'\blebanon\b|\blebanese\b|\bsyria|\bjordan|\biraq|\bgreece\b|\bgreek|\bturkey\b|\bturkish\b|\bcyprus\b|\bcypriot|\bmediterranean\b|\bEU\b|\btunisia|\bitaly\b|\bitalian\b|\beuropean\b|\b#lebanon\b|\b#lebanese\b|\b#syria|\b#jordan|\b#iraq|\b#greece\b|\b#greek|\b#turkey\b|\b#turkish\b|\b#cyprus\b|\b#cypriot|\b#mediterranean\b|\b#EU\b|\b#tunisia|\b#italy\b|\b#italian\b|\b#european\b'

regex_covid = re.compile(regex_string_covid, re.IGNORECASE)
regex_migrat = re.compile(regex_string_migrat, re.IGNORECASE)
regex_geos = re.compile(regex_string_geos, re.IGNORECASE)


# filter based on immigration and geos
data_filter_ig = []

for entry in all_data.get('data'):
    if regex_migrat.search(entry.get('text')) and regex_geos.search(entry.get('text')):
        data_filter_ig.append(entry)
len(data_filter_ig)


# adding covid variable

for entry in data_filter_ig:
    if regex_covid.search(entry.get('text')):
        entry['covid'] = 1
    else:
        entry['covid'] = 0


# Convert data to df

df_tweets = pd.DataFrame.from_records(data_filter_ig)
df_users = pd.DataFrame.from_records(all_data.get('includes').get('users'))


# Functions for unnesting
def fix_dicts(string):
    if string is np.nan:
        return(string)
    if not isinstance(string, dict):
        string_as_dict = ast.literal_eval(string)
        return(string_as_dict)
    else:
        return(string)

def unnest_hashtags(entities):
    try:
        hashtags = list(entities.get('hashtags'))
    except:
        return(list())
    if isinstance(hashtags, list):
        hashtags_list = [hashtag.get('tag') for hashtag in hashtags]
        return(hashtags_list)
    else:
        return
    
def unnest_mentions(entities):
    try:
        mentions = list(entities.get('mentions'))
    except:
        return(list())
    if isinstance(mentions, list):
        mentions_list = [mention.get('username') for mention in mentions]
        return(mentions_list)
    else:
        return

def unnest_urls(entities):
    try:
        urls = list(entities.get('urls'))
    except:
        return(list())
    if isinstance(urls, list):
        urls_list = [url.get('url') for url in urls]
        return(urls_list)
    else:
        return
    
def unnest_cashtags(entities):
    try:
        cashtags = list(entities.get('cashtags'))
    except:
        return(list())
    if isinstance(cashtags, list):
        cashtags_list = [cashtag.get('tag') for cashtag in cashtags]
        return(cashtags_list)
    else:
        return


# Functions for wrangling data frame
def wrangle_df_tweets(df, drop_cols):
    
    # Fix dictionaries
    df['public_metrics'] = df['public_metrics'].apply(fix_dicts)
    df['entities'] = df['entities'].apply(fix_dicts)
    
    # Unnest
    df = pd.concat([df, pd.json_normalize(df['public_metrics'])], axis = 1)
    df['hashtags'] = df['entities'].apply(unnest_hashtags)
    df['mentions'] = df['entities'].apply(unnest_mentions)
    df['urls'] = df['entities'].apply(unnest_urls)
    df['cashtags'] = df['entities'].apply(unnest_cashtags)
    df = df.loc[:, ~df.columns.isin(drop_cols)]
    
    return(df)

def wrangle_df_users(df, drop_cols):
    
    # Fix dicts
    df['public_metrics'] = df['public_metrics'].apply(fix_dicts)
    
    # Unnest
    df = pd.concat([df, pd.json_normalize(df['public_metrics'])], axis = 1)
    df = df.rename(columns = {'id': 'author_id', 'created_at': 'author_created_at'})
    df = df.loc[:, ~df.columns.isin(drop_cols)]
    
    return(df)


# Wrangle data frame
drop_cols = ['public_metrics', 'entities']

df_tweets_unnest = wrangle_df_tweets(df_tweets, drop_cols)
df_users_unnest = wrangle_df_users(df_users, drop_cols)

# Add referenced tweet info
df_tweets_unnest = df_tweets_unnest.explode('referenced_tweets')
df_tweets_unnest['referenced_type'] = np.nan
df_tweets_unnest['referenced_id'] = np.nan
df_tweets_unnest.loc[df_tweets_unnest['referenced_tweets'].notna(), 'referenced_type'] = df_tweets_unnest.loc[df_tweets_unnest['referenced_tweets'].notna(), 'referenced_tweets'].apply(lambda entry: entry.get('type'))
df_tweets_unnest.loc[df_tweets_unnest['referenced_tweets'].notna(), 'referenced_id'] = df_tweets_unnest.loc[df_tweets_unnest['referenced_tweets'].notna(), 'referenced_tweets'].apply(lambda entry: entry.get('id'))


# Combine data with pd.merge
df_combined = pd.merge(df_tweets_unnest, df_users_unnest, how = 'left', left_on = 'author_id', right_on = 'author_id').drop_duplicates(subset = ['id'])


# Recoding and adding variables
df_combined['covid'] = df_combined['covid'].astype(bool)
df_combined['tweet_link'] = 'https://twitter.com/' + df_combined['username'] + '/status/' + df_combined['id']
df_combined['id'] = df_combined['id'].astype('int64')


# Adding existing labels
df_combined = pd.merge(df_combined, labelled_df.loc[:, ['id', 'label']], on = 'id', how = 'left').loc[:, keep_columns]


# Export to excel
df_combined.to_excel(out_excel, index = False)

# Export prodigy set 01
df_tagset = df_combined.loc[df_combined['referenced_type'].isna(), ['id', 'username', 'text', 'tweet_link']]
df_tagset.to_json(out_tagset, orient = 'records')