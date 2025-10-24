'''
This scipt access the openalex API and extract papers within a specific
time window

Work object:
    [id, doi, title, publication_date]
    concepts:
    is_paratext:False to remove random stuff
    author_position: are first, middle, and last.
    abstract_inverted_index: needs reconstruction
    authorships
Author object:
    [id, orcid, display_name]
    last_known_institution
Concept object
    [id, display_name, ]
    counts_by_year: peak concepts with high frequency
    ancestors: where that concept descends from

OpenAlex ID: W(ork), A(uthor), V(enue), I(nstitution),|C(oncept)
negation:!, OR:|
filters: https://docs.openalex.org/api/get-lists-of-entities/filter-entity-lists
'''

import requests
import json
import datetime
import time
import pandas as pd


# %%
def call_openalex_api(query):
    try:
        response = requests.get(query, timeout=2)
    except requests.ConnectionError:
        response = requests.get(query, timeout=3)
    except requests.Timeout:
        time.sleep(1)
        response = requests.get(query, timeout=3)
    except:
        response = 0
    return response


# %%
# https://www.crossref.org/documentation/content-registration/
sort_by = "publication_date"
base_url = "https://api.openalex.org/"
mailto = "mailto=ssou@itu.dk"
per_page = 200
wrds1 = "2019-nCoV|COVID-19|SARS-CoV-2|HCoV-2019|hcov|NCOVID19|%22severe%20acute%20respiratory%20syndrome%20coronavirus%202%22|%22severe%20acute%20respiratory%20syndrome%20corona%20virus%202%22"
wrds2 = "|coronavirus%20Wuhan|coronavirus%20China|coronavirus%20novel|%22corona%20virus%22%20Wuhan|%22corona%20virus%22%20China|%22corona%20virus%22%20novel"
from_dates = pd.date_range(start='2019-12', end='2022-07', freq='MS', inclusive='both')
to_dates = pd.date_range(start='2019-12', end='2022-08', freq='M', inclusive='both')
loc = "abstract"

cov_result = []
for i, j in zip(from_dates, to_dates):
    from_date, to_date = str(i.to_period('D')), str(j.to_period('D'))
    period = f"from_publication_date:{from_date},to_publication_date:{to_date}"
    temp = {}
    # for loc in ['abstract', 'title']:
    for type in ["posted-content", "!posted-content"]:
        query_covid = f"{base_url}works?filter={loc}.search:{wrds1+wrds2},is_paratext:false,type:{type},{period}&{mailto}"
        response = call_openalex_api(query_covid)
        total = int(response['meta']['count'])
        temp[type] = total
    cov_result += [from_date] + list(temp.values())
    print(from_date, *temp.values())
    time.sleep(3)
