#!/usr/bin/env python
# coding: utf-8

# In[1]:


import wget
import nbimporter
import operator
import numpy as np


# In[2]:


meduza = "Британские организации, работающие над созданием вакцины от COVID-19, подвергаются хакерским атакам со стороны других государств, в частности, Ирана, России и Китая. Об этом пишет The Guardian со ссылкой на данные Национального центра кибербезопасности. Как отмечает издание, ни одна из атак пока не была успешной. Во всем мире сейчас разрабатывается несколько десятков различных видов вакцин от COVID-19.Британские организации, работающие над созданием вакцины от COVID-19, подвергаются хакерским атакам со стороны других государств, в частности, Ирана, России и Китая. Об этом пишет The Guardian со ссылкой на данные Национального центра кибербезопасности. Как отмечает издание, ни одна из атак пока не была успешной.Во всем мире сейчас разрабатывается несколько десятков различных видов вакцин от COVID-19."
vedomosti = "В Великобритании дальше всех в разработке вакцины продвинулись ученые из Института Дженнера в Оксфорде. Разрабатываемый там препарат уже запустили в производство параллельно с началом испытаний на людях — в случае, если они окажутся успешными, уже к сентябрю ученые рассчитывают получить до миллиона доз.Британские университеты и научные организации, работающие над вакциной от коронавирусной инфекции, стали жертвами хакерских атак, пишет The Guardian со ссылкой на экспертов по кибербезопасности. «Считается, что за хакерскими атаками стоят государства, включая Иран и Россию, эксперты также называют Китай в качестве вероятного виновного», – пишет британская газета. О том, что кибератаки на британские учреждения, занимающиеся исследованиями нового коронавируса, можно отследить к России и Ирану, также сообщает таблоид The Mail on SundayВ Великобритании дальше всех в разработке вакцины продвинулись ученые из Института Дженнера в Оксфорде. Разрабатываемый там препарат уже запустили в производство параллельно с началом испытаний на людях — в случае, если они окажутся успешными, уже к сентябрю ученые рассчитывают получить до миллиона доз.Британские университеты и научные организации, работающие над вакциной от коронавирусной инфекции, стали жертвами хакерских атак, пишет The Guardian со ссылкой на экспертов по кибербезопасности. «Считается, что за хакерскими атаками стоят государства, включая Иран и Россию, эксперты также называют Китай в качестве вероятного виновного», – пишет британская газета. О том, что кибератаки на британские учреждения, занимающиеся исследованиями нового коронавируса, можно отследить к России и Ирану, также сообщает таблоид The Mail on Sunday"


# In[3]:


import gensim
import gensim.downloader as api
# Get information about the model or dataset
api.info('word2vec-ruscorpora-300')

# Download
w2v_model = api.load("word2vec-ruscorpora-300")
w2v_model.most_similar('человек_NOUN')
##w2v_model.


# ### Text Preprocessing

# In[4]:


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


# In[5]:


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


# In[6]:


from ufal.udpipe import Model, Pipeline
import os
import re
import sys

def tag_ud(text='Текст нужно передать функции в виде строки!', modelfile='udpipe_syntagrus.model'):
    udpipe_model_url = 'https://rusvectores.org/static/models/udpipe_syntagrus.model'
    udpipe_filename = udpipe_model_url.split('/')[-1]

    if not os.path.isfile(modelfile):
        print('UDPipe model not found. Downloading...', file=sys.stderr)
        wget.download(udpipe_model_url)
        print('\nLoading the model...', file=sys.stderr)
    model = Model.load(modelfile)
    process_pipeline = Pipeline(model, 'tokenize', Pipeline.DEFAULT, Pipeline.DEFAULT, 'conllu')



    #print('Processing input...', file=sys.stderr)
    for line in text:
        output = process(process_pipeline, text=line)
        print(' '.join(output))
        #print(line)
        #print(text)
        # line = unify_sym(line.strip()) # здесь могла бы быть ваша функция очистки текста
    return output


# In[7]:


#text = open(textfile, 'r', encoding='utf-8').read()
meduza_tagged = tag_ud(text=["Британские организации, работающие над созданием вакцины от COVID-19, подвергаются хакерским атакам со стороны других государств, в частности, Ирана, России и Китая. Об этом пишет The Guardian со ссылкой на данные Национального центра кибербезопасности. Как отмечает издание, ни одна из атак пока не была успешной. Во всем мире сейчас разрабатывается несколько десятков различных видов вакцин от COVID-19.Британские организации, работающие над созданием вакцины от COVID-19, подвергаются хакерским атакам со стороны других государств, в частности, Ирана, России и Китая. Об этом пишет The Guardian со ссылкой на данные Национального центра кибербезопасности. Как отмечает издание, ни одна из атак пока не была успешной.Во всем мире сейчас разрабатывается несколько десятков различных видов вакцин от COVID-19."])
vedomosti_tagged = tag_ud(text=["В Великобритании дальше всех в разработке вакцины продвинулись ученые из Института Дженнера в Оксфорде. Разрабатываемый там препарат уже запустили в производство параллельно с началом испытаний на людях — в случае, если они окажутся успешными, уже к сентябрю ученые рассчитывают получить до миллиона доз.Британские университеты и научные организации, работающие над вакциной от коронавирусной инфекции, стали жертвами хакерских атак, пишет The Guardian со ссылкой на экспертов по кибербезопасности. «Считается, что за хакерскими атаками стоят государства, включая Иран и Россию, эксперты также называют Китай в качестве вероятного виновного», – пишет британская газета. О том, что кибератаки на британские учреждения, занимающиеся исследованиями нового коронавируса, можно отследить к России и Ирану, также сообщает таблоид The Mail on SundayВ Великобритании дальше всех в разработке вакцины продвинулись ученые из Института Дженнера в Оксфорде. Разрабатываемый там препарат уже запустили в производство параллельно с началом испытаний на людях — в случае, если они окажутся успешными, уже к сентябрю ученые рассчитывают получить до миллиона доз.Британские университеты и научные организации, работающие над вакциной от коронавирусной инфекции, стали жертвами хакерских атак, пишет The Guardian со ссылкой на экспертов по кибербезопасности. «Считается, что за хакерскими атаками стоят государства, включая Иран и Россию, эксперты также называют Китай в качестве вероятного виновного», – пишет британская газета. О том, что кибератаки на британские учреждения, занимающиеся исследованиями нового коронавируса, можно отследить к России и Ирану, также сообщает таблоид The Mail on Sunday"])
bad_tagged = tag_ud(text=["Тверской суд Москвы арестовал администратора паблика «Омбудсмен полиции» Игоря Худякова в рамках дела о распространении порнографии. Об этом сообщает «Интерфакс».Худяков арестован на два месяца, до 22 июля 2020 года. Его подозревают в преступлении, предусмотренного пунктами а) и б) части 3 статьи 242 УК РФ (незаконные изготовление и оборот порнографических материалов или предметов группой лиц по предварительному сговору с использованием интернета). Подозреваемым по делу также проходит создатель паблика Владимир Воронцов. По версии следствия, в 2018 году он распространил в социальных сетях интимные фотографии неназванной женщины; дело завели по ее заявлению. Воронцов также обвиняется в вымогательстве 300 тысяч рублей у бывшего полицейского за отказ от распространения личных фотографий. Сейчас основатель «Омбудсмена полиции» находится под арестом. Воронцов отрицает вину и связывает преследование со своей деятельностью по защите прав рядовых сотрудников полиции."])


# In[8]:


def get_result_vector(tagged_article):
    result = []
    for word in tagged_article:
        try:
            result.append(w2v_model.get_vector(word))
        except: 
            pass

    return np.array([x/300 for x in sum(result)])


# In[9]:


meduza_vector = get_result_vector(meduza_tagged)

vedomosti_vector = get_result_vector(vedomosti_tagged)

bad_vector = get_result_vector(bad_tagged)


# In[10]:


def vectors_similarity(v1, v2):
    return np.sum(v1 * v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


# In[11]:


print(vectors_similarity(vedomosti_vector, meduza_vector))
print(vectors_similarity(bad_vector, meduza_vector))
print(vectors_similarity(bad_vector, vedomosti_vector))


# In[ ]:




