# TPB log



#### 2021-12-09

- Tweets extracted from specified use handles (`materials/news_handles.txt`)
- Daterange: 2020-02-01 - 2021-12-08
- Collected using `scripts/get_twitter_data.py`



#### 2022-02-03

- Created demoset with simple filters using `scripts/create_demoset_tpb.py`



#### 2022-03-08

- Received labeled tweets from RA Eva B.
- Labels both as colour coded excel file or as tweets separated into several files
    - Note: The separate files is the correct version, as changed were made between colour coding and splitting into files (see below)
- From e-mail:
  - I started by colour coding the main Excel file like this:
  - Red - New Mobilities
  - Green - Blocked  mobilities
  - Blue - Physical  Stuckness
  - Orange - Surrounding  precarity and vulnerabilities
  - Yellow - Pandemic  precarity
    - Some tweets are not highlighted in any colours because I thought they were outside the scope of our research (i.e. they were about Search and Rescue operations in the Mediterranean, people drowning, civil society actions, EU policies that were not relevant for our focus and others) 
    - When I then created the new Excel files for each clusters and went through the tweets again, I refined and polished them, ***and moved some tweets from one cluster to the other (without going back to the main Excel document and changing colours)***. For instance, at the beginning I classified the topic of Syrian returns in different clusters (in the main Excel file) but in the end I moved all the tweets about Syrian returns in one thematic cluster (New mobilities). So this is just to say, that there are some minor differences between the colour-coding in the main Excel sheet and the tweets contained in the 5 different Excel sheets 
    - As regards the 5 Excel sheets for each thematic clusters, they are divided in sub-themes. You will see that some of them are highlighted, but this was just for me to recognise which tweets/articles were the most interesting ones. 



#### 2022-03-28

- Converted labelled tweets into combined file with label-variabel: `tpb_tweets_simple_labels_20220308.csv`
- Stored labelled tweets as json records: `tpb_tweets_simple-filter_labelled_20220308.json`
- Created filtered set based on updated filter conditions (See document "Filtering tweets for Tracking Pandemic Borderscapes_20220328.docx")
    - Filtered set: `tpb_tweets_filtered_20220328.xlsx`
    - Set created using `scripts/create_filteret-set_prodigy-set01_20220328.py`
    - Manual corrections:
        - Added filter in Excel
        - Column width
        - id-column as number
        - tweet_link clickable using macro:
        ```
        Sub ConvertTextURLsToHyperlinks()
            Dim Cell As Range
            For Each Cell In Intersect(Selection, ActiveSheet.UsedRange)
                If Cell <> "" Then
                    ActiveSheet.Hyperlinks.Add Cell, Cell.Value
                End If
            Next
        End Sub
        ```
- Created set for annotating: `data/prodigy/tpb_tagset01.json`
    - Excluded retweets
    - Did *not* exclude already labelled tweets
    

**Set up first instance of tagging**
- Initiated manual text classification instance (https://prodi.gy/docs/text-classification)
- Using `data/prodigy/tpb_tagset01.json`
- Running with `feed_overlap: True` to review annotations later
- Set up using bash `tpb_textcat.sh`:
```
#!/bin/bash

source prodigy/bin/activate

export PRODIGY_PORT="8080"
export PRODIGY_BASIC_AUTH_USER=""
export PRODIGY_BASIC_AUTH_PASS=""
export PRODIGY_ALLOWED_SESSIONS="eva,tamy,kristian,signe"

nohup  prodigy textcat.manual tpb_cat "./tpb/data/tpb_tagset01.json" --label "Physical stuckness","Surrounding precarity and vulnerabilities","Blocked or derailed mobilities","Pandemic precarity","New mobilities","Other" --exclusive &> nohup_tpb-cat_20220328.out &
```

- Sent filtered data and prodigy instructions to Eva and Tamy



#### 2022-04-08

- Converting labelled tweets from simple filter to prodigy format using script: `labelled-to-prodigy-format.py`

- Data in prodigy format stored to: `data/tpb_tweets_simple-filter_labelled-prodigy-format_20220408.json`

- Contains both labelled and non-labelled entries

  - Labelled: 303
  - Non-labelled (corresponding to "ignored"): 1121

- Uploading to prodigy instance

- Imported to prodigy database using: `prodigy db-in tpb_simple-filter_labelled_test ./tpb/data/tpb_tweets_simple-filter_labelled-prodigy-format_20220408.json`

- Training model using: `prodigy train --textcat tpb_simple-filter_labelled_test`:

  ![image-20220408144654463](.\img\image-20220408144654463.png)

- Train-curve using: `prodigy train-curve --textcat tpb_simple-filter_labelled_test --show-plot`:

  ![image-20220408144805234](.\img\image-20220408144805234.png)

  - Curve indicates that model could be improved
  - Also note low evaluation sample size (n = 60)

- Storing model as `tpb_labeller_test` - added to repository
  - Contains both `model_best` and `model_last` - difference unclear
- Manual evaluation using `notebooks/model_test.ipynb`
  - Model used like any other spacy model
  - `doc` contains `.cats` attribute for predicted label values (see https://spacy.io/api/textcategorizer)



#### 2022-04-11

- Creating new tagging sets based on meeting discussion

  - One with the tweets matching the covid filter
  - One without

- Crated two sets: `tpb_tagset_covid01.json` (375 tweets) and `tpb_tagset_other01.json` (2703 tweets)

  - Using script: `create-prodigy-sets_apr22.py`

- Shutting down previous tagging instance from march 28th 

- Using new categories:

  - Covid categories:
    - Physical stuckness and Covid
    - Pandemic precarity
    - Blocked and derailed mobilities because of Covid
    - New mobilities in relation to Covid
    - Other
  - Other/contextual categories:
    - The backdrop of physical stuckness
    - Existing precarity and vulnerabilities
    - Context of blocked and derailed mobilities
    - New mobilities and migratory routes 
    - Other

- Starting separate tagging instances using script `tpb_textcat_covid-contextual.sh`:

  ```
  source prodigy/bin/activate
  
  export PRODIGY_PORT="8080"
  export PRODIGY_BASIC_AUTH_USER="tpb"
  export PRODIGY_BASIC_AUTH_PASS="tagthetweets4days"
  export PRODIGY_ALLOWED_SESSIONS="eva,tamy,kristian,signe"
  
  nohup  prodigy textcat.manual tpb_covidcat "./tpb/data/tpb_tagset_covid01.json" --label "Physical stuckness and Covid","Pandemic precarity","Blocked and derailed mobilities because of Covid","New mobilities in relation to Covid","Other" &> nohup_tpb_covid-cat_20220411.out &
  
  
  export PRODIGY_PORT="8070"
  export PRODIGY_BASIC_AUTH_USER="tpb"
  export PRODIGY_BASIC_AUTH_PASS="tagthetweets4days"
  export PRODIGY_ALLOWED_SESSIONS="eva,tamy,kristian,signe"
  
  nohup  prodigy textcat.manual tpb_contextcat "./tpb/data/tpb_tagset_other01.json" --label "The backdrop of physical stuckness","Existing precarity and vulnerabilities","Context of blocked and derailed mobilities","New mobilities and migratory routes","Other" &> nohup_tpb_context-cat_20220411.out &
  ```



#### 2022-04-27

- Checking if more labelling is needed using: `prodigy train-curve --textcat-multilabel tpb_contextcat --show-plot`
  - NOTE: Data is *multilabelled*

![image-20220427110402551](.\img\image-20220427110402551.png)

- Creating script for converting prodigy format to excel file: `prodigy-format_to-excel.py`



#### 2022-04-29

**Export labelled COVID tweets**

- Ending COVID tagging instance and exporting labelled COVID-tweets to excel file: `tpb_covid-tweets_labelled.xlsx`

  - Using script: `prodigy-format_to-excel.py`
  - Labelled data exported from prodigy as `tpb_covidcat_labelled_20220429.jsonl`
  - **NOTE:** ID's in tagging sets rounded up - possible due to float point limitation in `json.dump()` - ***convert id's to strings before export in the future!***
    - Tweet ID reconstructed from tweet_link
  - Label names changed:
    - Physical stuckness and Covid: Physical stuckness and Covid
    - Pandemic precarity: Pandemic precarity
    - Blocked and derailed mobilities because of Covid: Blocked and derailed mobilities in relation to Covid
    - New mobilities in relation to Covid: Mobility in relation to Covid
    - Other: Other
  - Sorted by date (oldest to newest)
  - tweet-links made clickable
  - Exported as tidy: One row per label per tweet (tweets with two labels appearing twice)

- **New label names:**

  - In the Covid dataset:

    a. Physical stuckness and Covid

    b. Pandemic precarity

    **c. Blocked and derailed mobilities in relation to Covid**

    **d. Mobility in relation to Covid** 

    e. Other

  - In the contextual dataset:

    a. The backdrop of physical stuckness

    b. Existing precarity and vulnerabilities 

    c. Context of blocked and derailed mobilities 

    **d. Mobility along new and old routes** 

    e. Other 



**Training model**

- Checking if more labelling is needed for contextual tweets using: `prodigy train-curve --textcat-multilabel tpb_contextcat --show-plot`

  ![image-20220429105543052](.\img\image-20220429105543052.png)

- Training model using: `prodigy train tpb_labeller --textcat-multilabel tpb_contextcat`

  - Model named `tpb_labeller`



**Testing `textcat.correct`**

- **NOTE:** `textcat.py` (`prodigy/lib/python3.8/site-packages/prodigy/recipes`) recipe has been edited to always use "multiple" choice view (used single despite being multilabel)
  - Created backup: `textcat_bck.py`
- Testing `textcat.correct` recipe using: `prodigy textcat.correct tpb_contextcat_correct ./tpb/tpb_labeller/model-last "./tpb/data/tpb_tagset_other01.json" --threshold 0.8` (tpb_textcat_with-model.sh)
- **Alternatives:**
  - Annotate by correcting model
  - Annotate by only correcting tweets under a certain threshold



#### 2022-05-23

**Predicting labels**

- Using model `tpb_labeller` to predict labels for unlabelled tweets (unlabelled at 2022-04-29)
- Model `tpb_labeller` added to repo
- Exporting manually labelled data: `tpb_contextcat_20220523.jsonl`
- Started work on notebook for predicting label: `predict_context.ipynb`
  - Reads in labelled data and raw data
  - Converts labelled to tidy (one row per label)
  - Creates indicator for whether data was part of model training
    - NOTE: Possible to discern whether data was part of training or test?
  - Wrapper function for predicting context category



#### 2022-05-31

- Terminating contextcat instance (all tweets labelled)

- Creating script for manually splitting data in training and test: `create-train-test.py`

- Exporting labelled context-cat data (again): `tpb_contextcat_20220531.jsonl`

  - `prodigy db-out tpb_contextcat > ./tpb/data/tpb_contextcat_20220531.jsonl`

- Creating training set and test set using `create-train-test.py`

  - `prodigy db-in tpb_contextcat_test ~/tpb/data/tpb_contextcat_test.jsonl`
  - `prodigy db-in tpb_contextcat_train_20220531 ~/tpb/data/tpb_contextcat_train.jsonl`

- Re-creating `tpb_labeller` using manual train and test: `prodigy train ~/tpb/bp_tpb/models/tpb_labeller --textcat-multilabel tpb_contextcat_train_20220531,eval:tpb_contextcat_test `

  ![image-20220531145822216](.\img\image-20220531145822216.png)

- Adding new version of `tpb_labeller` and training data to repo

- Creating excel dataset for contextual tweets (using `predict_context.ipynb`):
  - Ignored tweets filtered out
  - All tweets not used for training predicted
  - Added column for predicted label and precision
  - Dataset: `tpb_context-tweets_labelled-predicted.xlsx`

- Created two visualization for precision of label prediction (added to `output` folder in repo)

