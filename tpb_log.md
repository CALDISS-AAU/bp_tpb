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