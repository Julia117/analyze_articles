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


for item in feed_lenta['items']:
    lenta_articles.append(get_text(item))


# Preprocess articles

import nltk
nltk.download("stopwords")
#--------#

from nltk.corpus import stopwords
from pymystem3 import Mystem
from string import punctuation

#Create lemmatizer and stopwords list
mystem = Mystem() 
russian_stopwords = stopwords.words("russian")

#Preprocess function
def preprocess_text(text):
    tokens = mystem.lemmatize(text.lower())
    tokens = [token for token in tokens if token not in russian_stopwords              and token != " "              and token.strip() not in punctuation]
    
    text = " ".join(tokens)
    
    return text


# In[50]:
print("hello")


preprocess_text("Ну что сказать, я вижу кто-то наступил на грабли, Ты разочаровал меня, ты был натравлен.")
#> 'сказать видеть кто-то наступать грабли разочаровывать натравлять'

preprocess_text("По асфальту мимо цемента, Избегая зевак под аплодисменты. Обитатели спальных аррондисманов")
#> 'асфальт мимо цемент избегать зевака аплодисменты обитатель спальный аррондисман'


# ### Compare articles

# In[16]:


from nltk.tokenize import word_tokenize, sent_tokenize

data = "Mars is a cold desert world. It is half the size of Earth. "


# In[98]:


print(sent_tokenize(data))
print(word_tokenize(data))


# In[17]:

print("hello")

file_docs = []

tokens = sent_tokenize(meduza_articles[0])
for line in tokens:
    file_docs.append(line)

print("Number of documents:",len(file_docs))


# In[112]:


gen_docs = [[w.lower() for w in word_tokenize(text)] 
            for text in file_docs]


# In[43]:


print(meduza_articles[18])
print(vedomosti_articles[1])


# In[ ]:


print("hello")



# In[22]:


from sklearn.feature_extraction.text import TfidfVectorizer
vect = TfidfVectorizer(min_df=1)  


# In[23]:


tfidf = vect.fit_transform(file_docs)


# In[27]:


pairwise_similarity = tfidf * tfidf.T 
pairwise_similarity.toarray()

print("hello")

# In[52]:


import nltk, string
from sklearn.feature_extraction.text import TfidfVectorizer

##nltk.download('punkt') # if necessary...


stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

def stem_tokens(tokens):
    return [stemmer.stem(item) for item in tokens]

def normalize(text):
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))

vectorizer = TfidfVectorizer(tokenizer=normalize)

def cosine_sim(text1, text2):
    tfidf = vectorizer.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0,1]


print (cosine_sim(preprocess_text(meduza_articles[0]), preprocess_text(meduza_articles[0])))
print (cosine_sim(preprocess_text(meduza_articles[18]), preprocess_text(vedomosti_articles[1])))


preprocess_text(meduza_articles[18])

preprocess_text(vedomosti_articles[1])

import gensim
dictionary = gensim.corpora.Dictionary(gen_docs)
print(dictionary.token2id)


corpus = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs]


# In[119]:


tf_idf = gensim.models.TfidfModel(corpus)


# ### test

# In[65]:


ved_preproc = [preprocess_text(item) for item in vedomosti_articles]


# In[90]:


meduza_preproc = [preprocess_text(item) for item in meduza_articles]


# In[91]:


print(ved_preproc[1])
print(meduza_preproc[18])


# In[92]:

"""" 
tagged_data


# In[67]:


#def make_tagged(data):
#    return [TaggedDocument(words=word_tokenize(_d.lower()), tags=[str(i)]) for i, _d in enumerate(data)]

labeled_questions=[]
labeled_questions.append(TaggedDocument(ved_preproc[i], df[df.index == i].qid1))
labeled_questions.append(TaggedDocument(questions2[i].split(), df[df.index == i].qid2))


# In[70]:


from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize

tagged_data = make_tagged(ved_preproc)
max_epochs = 100
vec_size = 20
alpha = 0.025

model = Doc2Vec(vector_size=vec_size,
                alpha=alpha, 
                min_alpha=0.00025,
                min_count=1,
                dm =1)
  
model.build_vocab(tagged_data)

for epoch in range(max_epochs):
    print('iteration {0}'.format(epoch))
    model.train(tagged_data,
                total_examples=model.corpus_count,
                epochs=model.iter)
    # decrease the learning rate
    model.alpha -= 0.0002
    # fix the learning rate, no decay
    model.min_alpha = model.alpha

model.save("d2v.model")
print("Model Saved")


# In[94]:





# In[93]:


model_doc2vec = Sequential()
model_doc2vec.add(Embedding(voacabulary_dim, 100, input_length=longest_document, weights=[training_weights], trainable=False))
model_doc2vec.add(LSTM(units=10, dropout=0.25, recurrent_dropout=0.25, return_sequences=True))
model_doc2vec.add(Flatten())
model_doc2vec.add(Dense(3, activation='softmax'))
model_doc2vec.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])


# In[75]:


from gensim.models.doc2vec import Doc2Vec

model= Doc2Vec.load("d2v.model")
#to find the vector of a document which is not in training data
test_data = word_tokenize(preprocess_text(meduza_articles[18]))
v1 = model.infer_vector(test_data)
print("V1_infer", v1)

# to find most similar doc using tags
similar_doc = model.docvecs.most_similar('1')
print(similar_doc)


# In[82]:


preprocess_text(vedomosti_articles[123])


# In[77]:


preprocess_text(meduza_articles[18])


# In[ ]:



"""
