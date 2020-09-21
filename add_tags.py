from analyze_articles import text_processing
from analyze_articles import file_handling
import numpy as np
from datetime import datetime



def add_tags_to_articles(articles, file, dates):
    tagged_articles = {}
    try:
        for date in articles:
            if datetime.strptime(date, "%Y/%m/%d").date() in dates:
                print(date)
                tagged_articles[date] = [text_processing.add_tags(text=text) for text in articles[date]]
    finally:
        file_handling.add_to_file(file, tagged_articles)
    return tagged_articles


def get_result_vector(tagged_article, w2v_model):
    result = []
    for word in tagged_article:
        try:
            result.append(w2v_model.get_vector(word))
        except:
            pass
    return np.array([x / len(sum(result)) for x in sum(result)]).tolist()


def article_to_vector(tagged_articles, w2v_model, dates, file):
    vectors = {}
    try:
        for date in tagged_articles:
            if datetime.strptime(date, "%Y/%m/%d").date() in dates:
                print(date)
                vectors[date] = [get_result_vector(article, w2v_model) for article in tagged_articles[date]]
    finally:
        file_handling.add_to_file(file, vectors)
    return vectors

# def similar_pairs_percentage(pairs, vectors1, vectors2):
#     num_of_pairs = []
#     for day in pairs:
#         if len(vectors1[day]) == 0 or (len(vectors2[day])) == 0:
#             num_of_pairs.append(0)
#         else:
#             num_of_pairs.append(len(pairs[day]) / (len(vectors1[day])*len(vectors2[day])))
#     return num_of_pairs


# def replace_0(dict):
#     for day in dict:
#         if  dict[day] == []:
#             dict[day] = [-1,-1]
#     return dict



