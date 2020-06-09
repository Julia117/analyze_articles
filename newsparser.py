#!/usr/bin/env python
# coding: utf-8


import feedparser

rss_meduza = "https://meduza.io/rss/all"
rss_vedomosti = "https://www.vedomosti.ru/rss/news"
rss_lenta = "https://lenta.ru/rss"

feed_meduza = feedparser.parse(rss_meduza)
feed_vedomosti = feedparser.parse(rss_vedomosti)
feed_lenta = feedparser.parse(rss_lenta)

meduza_articles = []
vedomosti_articles = []
lenta_articles = []


#functions

def is_news(item):
    if "news" in item['link']:
        return True
    else:
        return False

from newspaper import Article

def get_text_old(item):
    url = item['link']
    article = Article(url)
    article.download()
    article.parse()
    return article.text

import requests
from bs4 import BeautifulSoup
def get_text(item):
    url = item['link']
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    texts = soup.find_all('p')
    texts_list = []
    for string in texts:
        texts_list.append(string.text)
    return "".join(texts_list)

import datetime

now = datetime.datetime.now()
def get_todays_articles(feed):
    return [item for item in feed['items'] if item.published[0:16] == now.strftime("%a, %d %b %Y")]


for item in get_todays_articles(feed_meduza):
    #if is_news(item):
        meduza_articles.append(get_text(item))

for item in get_todays_articles(feed_vedomosti):
    vedomosti_articles.append(get_text(item))

for item in get_todays_articles(feed_lenta):
    lenta_articles.append(get_text(item))




# Preprocess articles
