from utility_functions import file_handling
from tag_articles import text_processing
import numpy as np
from datetime import datetime


def add_tags_to_articles(articles, file, dates):
    """
    Add part-of-speech tags to articles in format word_part-of-speech

    Parameters
    ----------
    articles : all articles for days in dates in format {date : [articles]}

    file : name of the file to read articles from

    dates : a list of dates to tag articles for, dates in datetime.date("%Y/%m/%d") format

    Returns
    -------
    tagged_articles
        Dictionary of articles with tags in format {date : [tagged articles]}
    """
    tagged_articles = {}
    try:
        for date in articles:
            if datetime.strptime(date, "%Y/%m/%d").date() in dates:
                print("Tags added for ", date)
                tagged_articles[date] = [text_processing.add_tags(text=text) for text in articles[date]]
    # in case of failure processed data will be saved
    finally:
        file_handling.add_to_file(file, tagged_articles)
    return tagged_articles


def text_to_vector(tagged_article, w2v_model):
    """
    Get vector for an article using word2vec model

    Parameters
    ----------
    tagged_article : article text with added part-of-speech tags

    w2v_model : word to vector model trained for Russian language.
                Info available at https://rusvectores.org/en/about/

    Returns
    -------
    A list of 300 float numbers

    Notes
    -----
    To calculate a vector for a text we get vectors for all the words
    in the text, sum them and divide by the length of the sum vector.

    """
    result = []
    for word in tagged_article:
        try:
            result.append(w2v_model.get_vector(word))
        except:
            pass
    return np.array([x / len(sum(result)) for x in sum(result)]).tolist()


def article_to_vector(tagged_articles, w2v_model, dates, file):
    """
    Get vector for an article using word2vec model

    Parameters
    ----------
    tagged_articles : a list of articles texts with added part-of-speech tags

    w2v_model : word to vector model trained for Russian language.
                Info available at https://rusvectores.org/en/about/

    dates : list of dates for which we want to get vectors
            dates in datetime.date("%Y/%m/%d") format

    file : name of the file to save vectors to


    Returns
    -------
    vectors
        A dictionary of vectors in {date : [vectors]} format

    """

    vectors = {}
    try:
        for date in tagged_articles:
            if datetime.strptime(date, "%Y/%m/%d").date() in dates:
                print("Vectors calculated for ", date)
                vectors[date] = [text_to_vector(article, w2v_model) for article in tagged_articles[date]]
    # in case of failure processed data will be saved
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



