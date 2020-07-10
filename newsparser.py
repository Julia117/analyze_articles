#!/usr/bin/env python
# coding: utf-8

from analyze_articles import text_processing


# functions

from newspaper import Article


def get_text_old(item):
    url = item['link']
    article = Article(url)
    article.download()
    article.parse()
    return article.text

import datetime

now = datetime.datetime.now()
def get_todays_articles(feed):
    return [item for item in feed['items'] if item.published[0:16] == now.strftime("%a, %d %b %Y")]


# Preprocess articles

import gensim.downloader as api

# Get information about the model or dataset
api.info('word2vec-ruscorpora-300')

# Download model
w2v_model = api.load("word2vec-ruscorpora-300")

import numpy as np

def get_result_vector(tagged_article):
    result = []
    for word in tagged_article:
        try:
            result.append(w2v_model.get_vector(word))
        except:
            pass

    return np.array([x / len(sum(result)) for x in sum(result)])


def vectors_similarity(v1, v2):
    return np.sum(v1 * v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


def compare_pairs(list1, list2):
    similar_articles = []
    i = 0
    for vec1 in list1:
        j = 0
        for vec2 in list2:
            if vectors_similarity(vec1, vec2) > 0.91:
                similar_articles.append([i, j])
            j += 1
        i += 1
    return similar_articles


rss_meduza = "https://meduza.io/rss/all"
rss_vedomosti = "https://www.vedomosti.ru/rss/news"
rss_kommersant = "https://www.kommersant.ru/RSS/news.xml"


#get today's articles

import feedparser


def get_articles_vectors(rss):
    articles = []
    feed = feedparser.parse(rss)
    for item in get_todays_articles(feed):
        articles.append(get_text_old(item))

    tagged_articles = [text_processing.add_tags(text=text) for text in articles]
    vectors = [get_result_vector(article) for article in tagged_articles]
    return vectors


meduza_vectors = get_articles_vectors(rss_meduza)
vedomosti_vectors = get_articles_vectors(rss_kommersant)
kommersant_vectors = get_articles_vectors(rss_kommersant)

# Compare articles

similar_pairs_mv = compare_pairs(meduza_vectors, vedomosti_vectors)
similar_pairs_vk = compare_pairs(vedomosti_vectors, kommersant_vectors)
