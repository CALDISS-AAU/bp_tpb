#!/usr/bin/env python3

# Packages
import requests
import os
import json
import time
from datetime import datetime, timedelta

# handles
with open(os.path.join("..", "materials", "news-handles.txt"), "r") as f:
    handles = f.read().split("\n")

# token and endpoint
with open(os.path.join("D:/", "repos", "tokens", "twitter_bearer.txt"), 'r') as f:
    bearer_token = f.read()

# twitter API endpoint
search_url = "https://api.twitter.com/2/tweets/search/all"

# set start time and end time
start_time = "2020-02-01T00:00:00Z"
end_time = "2021-12-08T00:00:00Z"

# set query parameters
query_string = ' OR '.join([f"(from:{handle})" for handle in handles])
query_params = {'query': query_string,
                'tweet.fields': 'entities,public_metrics,created_at,referenced_tweets',
                'expansions': 'author_id',
                'user.fields': 'created_at,description,public_metrics,url,verified', 
                'max_results': 500,
                'start_time': start_time,
                'end_time': end_time}

# functions for API requests
def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FullArchiveSearchPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.get(search_url, auth=bearer_oauth, params=params)
    #print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def initial():
    json_response = connect_to_endpoint(search_url, query_params)
    return(json_response)

def continued(next_token):
    new_params = query_params.copy()
    new_params['next_token'] = next_token
    json_response = connect_to_endpoint(search_url, new_params)
    return(json_response)

# initialize data collection
data = initial()
all_data = data.copy()
all_data.pop('meta', None)

used_next_tokens = []
next_token = data.get('meta').get('next_token')

# collect as long as there are new next tokens
if next_token is not None:
    while True:
        time.sleep(1)
        data = continued(next_token)
        all_data['data'] = all_data.get('data') + data.get('data')
        all_data['includes']['users'] = all_data.get('includes').get('users') + data.get('includes').get('users')

        used_next_tokens.append(next_token)

        next_token = data.get('meta').get('next_token')

        if next_token is None:
            break