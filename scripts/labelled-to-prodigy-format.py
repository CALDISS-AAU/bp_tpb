# Import packages

import json
import pandas as pd
import os

data_p = os.path.join('..', 'data', 'tpb_tweets_simple-filter_labelled_20220308.json')
data_excel = os.path.join('..', 'data', 'tpb_tweets_simple-filter.xlsx')
data_out = os.path.join('..', 'data', 'tpb_tweets_simple-filter_labelled-prodigy-format_20220408.json')

example = {'id': 1468056419417088000, 
           'username': 'AJEnglish', 
           'text': '“Now, supermarkets have become boutiques.”\n\nPalestinian refugees in Lebanon’s Shatila camp pushed to the brink amid aid crisis ⤵️ https://t.co/fzjWcNV8Az', 
           'tweet_link': 'https://twitter.com/AJEnglish/status/1468056419417088003', 
           '_input_hash': -388230415, 
           '_task_hash': 976743313, 
           'options': [{'id': 'Physical stuckness', 'text': 'Physical stuckness'}, 
                       {'id': 'Surrounding precarity and vulnerabilities', 'text': 'Surrounding precarity and vulnerabilities'}, 
                       {'id': 'Blocked or derailed mobilities', 'text': 'Blocked or derailed mobilities'}, 
                       {'id': 'Pandemic precarity', 'text': 'Pandemic precarity'}, 
                       {'id': 'New mobilities', 'text': 'New mobilities'}, 
                       {'id': 'Other', 'text': 'Other'}], 
           '_view_id': 'choice', 
           'accept': ['Surrounding precarity and vulnerabilities'], 
           'config': {'choice_style': 'single'}, 
           'answer': 'accept', 
           '_timestamp': 1648628028, 
           '_annotator_id': 'tpb_cat-eva', 
           '_session_id': 'tpb_cat-eva'}

# Read data files
tweets_simple_filt = pd.read_excel(data_excel)

with open(data_p, 'r') as f:
    data = json.load(f)
    
# Filter not labelled - convert to records
data_notlabelled = tweets_simple_filt.loc[~tweets_simple_filt['id'].isin([entry.get('id') for entry in data]), ['username', 'text', 'id']]
data_notlabelled = data_notlabelled.to_dict(orient = 'records')

# Convert labelled to prodigy format
data_prodigy = []

for entry in data:
    new_entry = {}
    new_entry['id'] = entry.get('id')
    new_entry['username'] = entry.get('name')
    new_entry['text'] = list(tweets_simple_filt.loc[tweets_simple_filt['id'] == entry.get('id'), 'text'])[0]
    new_entry['options'] =[{'id': 'physical stuckness', 'text': 'physical stuckness'}, 
                           {'id': 'surrounding precarity and vulnerabilities', 'text': 'surrounding precarity and vulnerabilities'}, 
                           {'id': 'blocked mobilities', 'text': 'blocked mobilities'}, 
                           {'id': 'pandemic precarity', 'text': 'pandemic precarity'}, 
                           {'id': 'new mobilities', 'text': 'new mobilities'}]
    new_entry['accept'] = [entry.get('label')]
    new_entry['answer'] = 'accept'
    
    data_prodigy.append(new_entry)
    
    
# Convert non-labelled to prodigy forma
for entry in data_notlabelled:
    new_entry = {}
    new_entry['id'] = entry.get('id')
    new_entry['username'] = entry.get('username')
    new_entry['text'] = entry.get('text')
    new_entry['options'] =[{'id': 'physical stuckness', 'text': 'physical stuckness'}, 
                           {'id': 'surrounding precarity and vulnerabilities', 'text': 'surrounding precarity and vulnerabilities'}, 
                           {'id': 'blocked mobilities', 'text': 'blocked mobilities'}, 
                           {'id': 'pandemic precarity', 'text': 'pandemic precarity'}, 
                           {'id': 'new mobilities', 'text': 'new mobilities'}]
    new_entry['accept'] = []
    new_entry['answer'] = 'ignore'
    
    data_prodigy.append(new_entry)
    
    
# Save as json records
with open(data_out, 'w') as f:
    json.dump(data_prodigy, f)