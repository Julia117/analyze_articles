from utility_functions import file_handling
from newspaper import Article
from datetime import datetime


def get_text(url):
    """
    Get article text

    Parameters
    ----------
    url : link to download text from

    Returns
    -------
    Article text as string

    """

    article = Article(url)
    article.download()
    article.parse()
    return article.text


def get_articles_for_period(links, file, date_raw_list):
    """
    Get all articles for a period of time

    Parameters
    ----------
    links : list of all links for a time period in format {date : [links]}

    file : name of the file to save articles to

    date_raw_list : list of dates for which we want to download articles
                    dates in datetime.date("%Y/%m/%d") format

    Returns
    -------
    Saves articles to file

    Notes
    -----
    Date is saved to file so that we could import it later instead of
    downloading it. Downloading articles can take too long.

    """
    articles = {}
    try:
        for date in links:
            if datetime.strptime(date, "%Y/%m/%d").date() in date_raw_list:
                print("Articles downloaded for ", date)
                texts = []

                for link in links[date]:
                    try:
                        text = get_text(link)
                    except:
                        text = "ERROR"
                    if text:
                        texts.append(text)

                articles[date] = texts
    # in case of failure processed data will be saved
    finally:
        # print(list(articles.keys())[len(articles.keys())-1])
        file_handling.add_to_file(file, articles)
    return articles


