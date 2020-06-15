#!/usr/bin/env python
# coding: utf-8


import feedparser

rss_meduza = "https://meduza.io/rss/all"
rss_vedomosti = "https://www.vedomosti.ru/rss/news"
rss_lenta = "https://www.kommersant.ru/RSS/news.xml"

feed_meduza = feedparser.parse(rss_meduza)
feed_vedomosti = feedparser.parse(rss_vedomosti)
feed_lenta = feedparser.parse(rss_lenta)

meduza_articles = []
vedomosti_articles = []
lenta_articles = []


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

for item in get_todays_articles(feed_lenta):
    lenta_articles.append(get_text_old(item))

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


def clean_token(token, misc):
    """
    :param token:
    :param misc:
    :return:
    """
    out_token = token.strip().replace(' ', '')
    if token == 'Файл' and 'SpaceAfter=No' in misc:
        return None
    return out_token


def clean_lemma(lemma, pos, lowercase=True):
    """
    :param lemma:
    :param pos:
    :return:
    """
    out_lemma = lemma.strip().replace(' ', '').replace('_', '')
    if lowercase:
        out_lemma = out_lemma.lower()
    if '|' in out_lemma or out_lemma.endswith('.jpg') or out_lemma.endswith('.png'):
        return None
    if pos != 'PUNCT':
        if out_lemma.startswith('«') or out_lemma.startswith('»'):
            out_lemma = ''.join(out_lemma[1:])
        if out_lemma.endswith('«') or out_lemma.endswith('»'):
            out_lemma = ''.join(out_lemma[:-1])
        if out_lemma.endswith('!') or out_lemma.endswith('?') or out_lemma.endswith(',')                 or out_lemma.endswith('.'):
            out_lemma = ''.join(out_lemma[:-1])
    return out_lemma


def num_replace(word):
    newtoken = 'x' * len(word)
    nw = newtoken + '_NUM'
    return nw


def process(pipeline, text='Строка', keep_pos=True, keep_punct=False):
    entities = {'PROPN'}
    named = False
    memory = []
    mem_case = None
    mem_number = None
    tagged_propn = []

    # обрабатываем текст, получаем результат в формате conllu:
    processed = pipeline.process(text)

    # пропускаем строки со служебной информацией:
    content = [l for l in processed.split('\n') if not l.startswith('#')]

    # извлекаем из обработанного текста леммы, тэги и морфологические характеристики
    tagged = [w.split('\t') for w in content if w]

    for t in tagged:
        if len(t) != 10:
            continue
        (word_id, token, lemma, pos, xpos, feats, head, deprel, deps, misc) = t
        token = clean_token(token, misc)
        lemma = clean_lemma(lemma, pos)
        if not lemma or not token:
            continue
        if pos in entities:
            if '|' not in feats:
                tagged_propn.append('%s_%s' % (lemma, pos))
                continue
            morph = {el.split('=')[0]: el.split('=')[1] for el in feats.split('|')}
            if 'Case' not in morph or 'Number' not in morph:
                tagged_propn.append('%s_%s' % (lemma, pos))
                continue
            if not named:
                named = True
                mem_case = morph['Case']
                mem_number = morph['Number']
            if morph['Case'] == mem_case and morph['Number'] == mem_number:
                memory.append(lemma)
                if 'SpacesAfter=\\n' in misc or 'SpacesAfter=\s\\n' in misc:
                    named = False
                    past_lemma = '::'.join(memory)
                    memory = []
                    tagged_propn.append(past_lemma + '_PROPN ')
            else:
                named = False
                past_lemma = '::'.join(memory)
                memory = []
                tagged_propn.append(past_lemma + '_PROPN ')
                tagged_propn.append('%s_%s' % (lemma, pos))
        else:
            if not named:
                if pos == 'NUM' and token.isdigit():  # Заменяем числа на xxxxx той же длины
                    lemma = num_replace(token)
                tagged_propn.append('%s_%s' % (lemma, pos))
            else:
                named = False
                past_lemma = '::'.join(memory)
                memory = []
                tagged_propn.append(past_lemma + '_PROPN ')
                tagged_propn.append('%s_%s' % (lemma, pos))

    if not keep_punct:
        tagged_propn = [word for word in tagged_propn if word.split('_')[1] != 'PUNCT']
    if not keep_pos:
        tagged_propn = [word.split('_')[0] for word in tagged_propn]
    return tagged_propn


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
    print(i, j)
    return similar_articles


# Compare articles

meduza_tagged = [add_tags(text=text) for text in meduza_articles]
vedomosti_tagged = [add_tags(text=text) for text in vedomosti_articles]
lenta_tagged = [add_tags(text=text) for text in lenta_articles]

meduza_vectors = [get_result_vector(article) for article in meduza_tagged]
vedomosti_vectors = [get_result_vector(article) for article in vedomosti_tagged]

print(vectors_similarity(get_result_vector(meduza_tagged[1]), get_result_vector(vedomosti_tagged[1])))

sim_mv = compare_pairs(meduza_tagged, vedomosti_tagged)
