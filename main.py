from analyze_articles import get_articles
from analyze_articles import modify_files
from analyze_articles import file_handling
import gensim.downloader as api
import matplotlib.pyplot as plt


URLS_MEDUZA = "analyze_articles/urls_meduza.txt"
URLS_VEDOMOSTI = "analyze_articles/urls_vedomosti.txt"
URLS_KOMMERSANT = "analyze_articles/urls_kommersant.txt"

TEXTS_MEDUZA = "analyze_articles/texts_meduza.txt"
TEXTS_VEDOMOSTI = "analyze_articles/texts_vedomosti.txt"
TEXTS_KOMMERSANT = "analyze_articles/texts_kommersant.txt"

TAGGED_MEDUZA = "analyze_articles/tagged_meduza.txt"
TAGGED_VEDOMOSTI = "analyze_articles/tagged_vedomosti.txt"
TAGGED_KOMMERSANT = "analyze_articles/tagged_kommersant.txt"

VECTORS_MEDUZA = "analyze_articles/vectors_meduza.txt"
VECTORS_VEDOMOSTI = "analyze_articles/vectors_vedomosti.txt"
VECTORS_KOMMERSANT = "analyze_articles/vectors_kommersant.txt"

import datetime
date_raw = datetime.date(2020, 8 , 10)

urls_v = get_articles.get_links_since_date(date_raw, get_articles.get_links_for_date_vedomosti)
urls_k = get_articles.get_links_since_date(date_raw, get_articles.get_links_for_date_kommersant)
urls_m = get_articles.get_links_since_date_meduza(date_raw)

get_articles.get_articles_since_date(urls_m, TEXTS_MEDUZA)


with open("analyze_articles/urls_m.txt") as json_file:
    urls_m = json.load(json_file)

with open(TEXTS_KOMMERSANT) as json_file:
    articles_k = json.load(json_file)
with open(TEXTS_VEDOMOSTI) as json_file:
    articles_v = json.load(json_file)

with open(TEXTS_MEDUZA) as json_file:
    articles_m = json.load(json_file)
#####################################

# Get information about the model or dataset
api.info('word2vec-ruscorpora-300')
# Download model
w2v_model = api.load("word2vec-ruscorpora-300")
