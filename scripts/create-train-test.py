#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import json
import re
from datetime import datetime
import random

in_n = 'tpb_contextcat_20220523.jsonl'

data_p = os.path.join('..', 'data')
sets_out = os.path.join(data_p, 'prodigy')

data_in_p = os.path.join(data_p, in_n)


# loading data
with open(data_in_p, 'r') as f:
    data = [json.loads(line) for line in f]

# recreate id from link
id_regex = re.compile(r'(?<=/)(\d{15,20})$')

for entry in data:
    entry['id'] = id_regex.search(entry['tweet_link']).group(1)

    
# Use data labelled on April 29th to train model
filter_timestamp = datetime.timestamp(datetime.fromisoformat('2022-04-29T23:59:59'))

# Select data for training model
data_model = []

for entry in data:
    if entry['_timestamp'] < filter_timestamp:
        data_model.append(entry)

# Shuffle data and split into train and test
random.seed(4268)
random.shuffle(data_model)

n_test = round(0.2 * len(data_model)) # Using 20% for test

train_data = data_model[n_test:]
test_data = data_model[:n_test]

# Export sets
train_out_p = os.path.join(sets_out, 'tpb_contextcat_train.jsonl')
test_out_p = os.path.join(sets_out, 'tpb_contextcat_test.jsonl')

with open(train_out_p, 'w') as outfile:
    for entry in train_data:
        json.dump(entry, outfile)
        outfile.write('\n')

with open(test_out_p, 'w') as outfile:
    for entry in test_data:
        json.dump(entry, outfile)
        outfile.write('\n')

