from analyze_articles import get_articles
import json

TEXTS_MEDUZA = "analyze_articles/texts_m.txt"
TEXTS_VEDOMOSTI = "analyze_articles/texts_v.txt"
TEXTS_KOMMERSANT = "analyze_articles/texts_k.txt"

import datetime
date_raw = datetime.date(2020, 8 , 10)

urls_v = get_articles.get_links_since_date(date_raw, get_articles.get_links_for_date_vedomosti)
urls_k = get_articles.get_links_since_date(date_raw, get_articles.get_links_for_date_kommersant)
urls_m = get_articles.get_links_since_date_meduza(date_raw)

get_articles.get_articles_since_date(urls_m, TEXTS_VEDOMOSTI)

with open("analyze_articles/urls_kommersant.txt") as json_file:
    urls = json.load(json_file)

with open(TEXTS_KOMMERSANT) as json_file:
    articles = json.load(json_file)
