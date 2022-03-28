#!/usr/bin/env python
# coding: utf-8

# Import packages
import pandas as pd
import ast 
import numpy as np
import json
import re
import os

data_dir = os.path.join("..", "data")
data_path = os.path.join(data_dir, "tpb_df.csv")


# regex patterns

geolist = ["lebanon", "syria", "jordan", "iraq", "greece", "turkey", "cyprus", "mediterranean", "EU"]
wordlist = ["migrant", "refugee", "transit", "displacement", "border", "return", "pushback", "boat", "drowning", "hunger"]

regex_geo = re.compile("|".join([f"\\b{geo}\\b" for geo in geolist]), re.IGNORECASE)
regex_words = re.compile("|".join([f"\\b{word}" for word in wordlist]), re.IGNORECASE)
regex_hashtags = re.compile("|".join([f"\\b#{word}" for word in wordlist]), re.IGNORECASE)


# create subset

df = pd.read_csv(data_path)

keep_columns = ['created_at', 'name', 'text', 'hashtags', 'urls', 'retweet_count', 
                'reply_count', 'like_count', 'quote_count']

df_sub = df.loc[df['text'].apply(lambda t: (bool(regex_words.search(t)) or bool(regex_hashtags.search(t))) and bool(regex_geo.search(t))), keep_columns]


# comparison 

print(df.shape,
      df_sub.shape)


# export

df_sub.to_excel(os.path.join(data_dir, "tpb_tweets_simple-filter.xlsx"), index = False)

