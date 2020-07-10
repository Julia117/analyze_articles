#!/usr/bin/env python
# coding: utf-8

from analyze_articles import text_processing

import feedparser

rss_meduza = "https://meduza.io/rss/all"
rss_vedomosti = "https://www.vedomosti.ru/rss/news"
rss_kommersant = "https://www.kommersant.ru/RSS/news.xml"

feed_meduza = feedparser.parse(rss_meduza)
feed_vedomosti = feedparser.parse(rss_vedomosti)
feed_kommersant = feedparser.parse(rss_kommersant)

meduza_articles = []
vedomosti_articles = []
kommersant_articles = []


# functions

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
    result = "".join(texts_list)
    return result.replace("\xa0", " ")


import datetime

now = datetime.datetime.now()


def get_todays_articles(feed):
    return [item for item in feed['items'] if item.published[0:16] == now.strftime("%a, %d %b %Y")]


for item in get_todays_articles(feed_meduza):
    meduza_articles.append(get_text_old(item))

for item in get_todays_articles(feed_vedomosti):
    vedomosti_articles.append(get_text_old(item))

for item in get_todays_articles(feed_kommersant):
    kommersant_articles.append(get_text_old(item))

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
    result = "".join(texts_list)
    return result.replace("\xa0", " ")


# Preprocess articles

import wget
import numpy as np

import gensim.downloader as api

# Get information about the model or dataset
api.info('word2vec-ruscorpora-300')

# Download
w2v_model = api.load("word2vec-ruscorpora-300")


def clean_token(token, misc):
    """
    :param token:
    :param misc:
    :return:
    """
    out_token = token.strip().replace(' ', '')


# Preprocess articles
import wget

import gensim.downloader as api

# Get information about the model or dataset
api.info('word2vec-ruscorpora-300')

# Download
w2v_model = api.load("word2vec-ruscorpora-300")
from ufal.udpipe import Model, Pipeline
import os
import sys


def add_tags(text='Текст нужно передать функции в виде строки!', modelfile='udpipe_syntagrus.model'):
    udpipe_model_url = 'https://rusvectores.org/static/models/udpipe_syntagrus.model'
    udpipe_filename = udpipe_model_url.split('/')[-1]

    if not os.path.isfile(modelfile):
        print('UDPipe model not found. Downloading...', file=sys.stderr)
        wget.download(udpipe_model_url)
        print('\nLoading the model...', file=sys.stderr)
    model = Model.load(modelfile)
    process_pipeline = Pipeline(model, 'tokenize', Pipeline.DEFAULT, Pipeline.DEFAULT, 'conllu')
    output = []
    # print('Processing input...', file=sys.stderr)
    # for line in text:
    output = process(process_pipeline, text=text)

    # print(' '.join(output))
    # line = unify_sym(line.strip()) # здесь могла бы быть ваша функция очистки текста
    return output


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


# Compare articles

meduza_tagged = [add_tags(text=text) for text in meduza_articles]
vedomosti_tagged = [add_tags(text=text) for text in vedomosti_articles]
kommersant_tagged = [add_tags(text=text) for text in kommersant_articles]

meduza_vectors = [get_result_vector(article) for article in meduza_tagged]
vedomosti_vectors = [get_result_vector(article) for article in vedomosti_tagged]
kommersant_vectors = [get_result_vector(article) for article in kommersant_tagged]

print(vectors_similarity(get_result_vector(meduza_tagged[1]), get_result_vector(vedomosti_tagged[1])))

sim_mv = compare_pairs(meduza_vectors, vedomosti_vectors)
sim_vk = compare_pairs(vedomosti_vectors, kommersant_vectors)

# Clustering

from sklearn.cluster import KMeans
import numpy as np

kmeans = KMeans(n_clusters=3, random_state=0).fit(vedomosti_vectors)
kmeans.labels_
kmeans.cluster_centers_




# k-means clustering
from numpy import unique
from numpy import where
from sklearn.datasets import make_classification
from sklearn.cluster import KMeans
from matplotlib import pyplot
# define dataset
X, _ = make_classification(n_samples=1000, n_features=2, n_informative=2, n_redundant=0, n_clusters_per_class=1, random_state=4)
# define the model
model = KMeans(n_clusters=2)
# fit the model
model.fit(X)
# assign a cluster to each example
yhat = model.predict(X)
# retrieve unique clusters
clusters = unique(yhat)
# create scatter plot for samples from each cluster
for cluster in clusters:
	# get row indexes for samples with this cluster
	row_ix = where(yhat == cluster)
	# create scatter of these samples
	pyplot.scatter(X[row_ix, 0], X[row_ix, 1])
# show the plot
pyplot.show()


# k-means clustering
from numpy import unique
from numpy import where
from sklearn.datasets import make_classification
from sklearn.cluster import KMeans
from matplotlib import pyplot
# define dataset
#X, _ = make_classification(n_samples=1000, n_features=2, n_informative=2, n_redundant=0, n_clusters_per_class=1, random_state=4)
# define the model
model = KMeans(n_clusters=3)
model.fit(kommersant_vectors)
# assign a cluster to each example
identified_clusters = model.fit_predict(kommersant_vectors)
# retrieve unique clusters
data = kommersant_vectors.copy()
data.cluster = identified_clusters

clusters = unique(yhat)
# create scatter plot for samples from each cluster
for cluster in clusters:
	# get row indexes for samples with this cluster
	row_ix = where(yhat == cluster)
	# create scatter of these samples
	pyplot.scatter(kommersant_vectors[row_ix, 0], X[row_ix, 1])
# show the plot
pyplot.show()