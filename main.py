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
date_start = datetime.date(2020, 3, 1)
date_end = datetime.date(2020, 5, 31)
period = get_articles.date_range(date_start, date_end)
# period = get_articles.get_missing_dates(date_start, date_end, VECTORS_KOMMERSANT)

#download links for articles (date: links)
urls_v = get_articles.get_links_for_period(period, get_articles.get_links_for_date_vedomosti)
urls_k = get_articles.get_links_for_period(period, get_articles.get_links_for_date_kommersant)
urls_m = get_articles.get_links_for_period_meduza(period)


###or read links from file
urls_m = file_handling.read_from_file(URLS_MEDUZA)
urls_k = file_handling.read_from_file(URLS_KOMMERSANT)
urls_v = file_handling.read_from_file(URLS_VEDOMOSTI)


#download articles texts
get_articles.get_articles_for_period(urls_m, TEXTS_MEDUZA, period)
get_articles.get_articles_for_period(urls_v, TEXTS_VEDOMOSTI, period)
get_articles.get_articles_for_period(urls_k, TEXTS_KOMMERSANT, period)

###or read articles from file
articles_k = file_handling.read_from_file(TEXTS_KOMMERSANT)
articles_v = file_handling.read_from_file(TEXTS_VEDOMOSTI)
articles_m = file_handling.read_from_file(TEXTS_MEDUZA)

#####################################

# Get information about the model or dataset
api.info('word2vec-ruscorpora-300')
# Download model
w2v_model = api.load("word2vec-ruscorpora-300")

#add tags to texts
modify_files.add_tags_to_articles(articles_m, TAGGED_MEDUZA, period)
modify_files.add_tags_to_articles(articles_v, TAGGED_VEDOMOSTI, period)
modify_files.add_tags_to_articles(articles_k, TAGGED_KOMMERSANT, period)

###or read tagged articles from file
tagged_m = file_handling.read_from_file(TAGGED_MEDUZA)
tagged_v = file_handling.read_from_file(TAGGED_VEDOMOSTI)
tagged_k = file_handling.read_from_file(TAGGED_KOMMERSANT)

#convert texts to vectors
vectors_m = modify_files.artice_to_vector(tagged_m, w2v_model, period, VECTORS_MEDUZA)
vectors_v = modify_files.artice_to_vector(tagged_v, w2v_model, period, VECTORS_VEDOMOSTI)
vectors_k = modify_files.artice_to_vector(tagged_k, w2v_model, period, VECTORS_KOMMERSANT)

###or read vectors from file
vectors_m = file_handling.read_from_file(VECTORS_MEDUZA)
vectors_k = file_handling.read_from_file(VECTORS_KOMMERSANT)
vectors_v = file_handling.read_from_file(VECTORS_VEDOMOSTI)


# make pairwise comparison of the papers, find pairs that cover 92% similar topics
similar_vm = modify_files.compare_pairs(vectors_v, vectors_m)
similar_vk = modify_files.compare_pairs(vectors_v, vectors_k)
similar_mk = modify_files.compare_pairs(vectors_m, vectors_k)


#draw the plot
modify_files.make_plot(vectors_m, vectors_k, vectors_v)
plt.close()