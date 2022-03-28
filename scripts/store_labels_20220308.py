# Import packages
import pandas as pd
import ast 
import numpy as np
import json
import re
import os

# Set paths
data_dir = os.path.join("..", "data")
labelled_path = os.path.join(data_dir, "tpb_tweets_simple_labels_20220308.csv")
out_p = os.path.join(data_dir, "tpb_tweets_simple-filter_labelled_20220308.json")

# Read data
tweets_labelled = pd.read_csv(labelled_path, sep = ";")
tweets_labelled.columns = ['created_at', 'name', 'tweet_url', 'label']

# Re-create id-column
tweets_labelled['id'] = tweets_labelled['tweet_url'].str.extract(r'(\d+)$').astype('int64')

# Select columns
tweets_labelled_s = tweets_labelled.loc[:, ['created_at', 'name', 'id', 'label']]

# Store as json records
tweets_labelled_s.to_json(out_p, orient = "records")