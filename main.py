from analyze_articles import plots, util_functions, file_handling
from tag_articles import add_tags, find_pairs
from download_articles import get_articles, get_links
import gensim.downloader as api


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
date_end = datetime.date(2020, 9, 3)
period = util_functions.date_range(date_start, date_end)
# period = util_functions.get_missing_dates(date_start, date_end, VECTORS_KOMMERSANT)

# download links for articles (date: links) and add links to files
urls_v = get_links.get_links_for_period(period, get_links.get_links_for_date_vedomosti)
urls_k = get_links.get_links_for_period(period, get_links.get_links_for_date_kommersant)
urls_m = get_links.get_links_for_period_meduza(period)

file_handling.add_to_file(URLS_MEDUZA, urls_m)
file_handling.add_to_file(URLS_VEDOMOSTI, urls_v)
file_handling.add_to_file(URLS_KOMMERSANT, urls_k)

### or read links from file
urls_m = file_handling.read_from_file(URLS_MEDUZA)
urls_k = file_handling.read_from_file(URLS_KOMMERSANT)
urls_v = file_handling.read_from_file(URLS_VEDOMOSTI)


# download articles texts
get_articles.get_articles_for_period(urls_m, TEXTS_MEDUZA, period)
get_articles.get_articles_for_period(urls_v, TEXTS_VEDOMOSTI, period)
get_articles.get_articles_for_period(urls_k, TEXTS_KOMMERSANT, period)

### or read articles from file
articles_k = file_handling.read_from_file(TEXTS_KOMMERSANT)
articles_v = file_handling.read_from_file(TEXTS_VEDOMOSTI)
articles_m = file_handling.read_from_file(TEXTS_MEDUZA)

#####################################

# Get information about the model or dataset
api.info('word2vec-ruscorpora-300')
# Download model
w2v_model = api.load("word2vec-ruscorpora-300")

# add tags to texts
add_tags.add_tags_to_articles(articles_m, TAGGED_MEDUZA, period)
add_tags.add_tags_to_articles(articles_v, TAGGED_VEDOMOSTI, period)
add_tags.add_tags_to_articles(articles_k, TAGGED_KOMMERSANT, period)

### or read tagged articles from file
tagged_m = file_handling.read_from_file(TAGGED_MEDUZA)
tagged_v = file_handling.read_from_file(TAGGED_VEDOMOSTI)
tagged_k = file_handling.read_from_file(TAGGED_KOMMERSANT)

# convert texts to vectors
vectors_m = add_tags.article_to_vector(tagged_m, w2v_model, period, VECTORS_MEDUZA)
vectors_v = add_tags.article_to_vector(tagged_v, w2v_model, period, VECTORS_VEDOMOSTI)
vectors_k = add_tags.article_to_vector(tagged_k, w2v_model, period, VECTORS_KOMMERSANT)

### or read vectors from file
vectors_m = file_handling.read_from_file(VECTORS_MEDUZA)
vectors_k = file_handling.read_from_file(VECTORS_KOMMERSANT)
vectors_v = file_handling.read_from_file(VECTORS_VEDOMOSTI)


# make pairwise comparison of the papers, find pairs that cover 92% similar topics
similar_vm = find_pairs.compare_pairs(vectors_v, vectors_m)
similar_vk = find_pairs.compare_pairs(vectors_v, vectors_k)
similar_mk = find_pairs.compare_pairs(vectors_m, vectors_k)


# draw the plot
plots.make_plot(vectors_m, vectors_k, vectors_v)

# close plot
# plt.close()
