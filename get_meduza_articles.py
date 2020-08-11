from newspaper import Article
import requests
import datetime
import json


date_raw = datetime.date(2020, 6, 5)
date = date_raw.strftime("%Y/%m/%d")


def get_text(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.text


def write_to_file(filename, new):
    with open(filename, "w") as outfile:
        json.dump(new, outfile)


def merge_articles_data(dict1, dict2):
    result = {}
    for key in (dict1.keys() | dict2.keys()):
        result.setdefault(key, [])
        if key in dict1: result[key] += dict1[key]
        if key in dict2: result[key] += dict2[key]
    return result


def get_articles_since_date(date_raw):
    previous_date = (date_raw - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    articles_urls_list = []
    date_is_reached = False
    i = 0

    articles_before = {}
    while not date_is_reached:
        url = "https://meduza.io/api/v3/search?chrono=news&locale=ru&page=" + str(i) + "&per_page=100"
        response = requests.get(url)
        json_data = response.json()

        info = json_data['documents']
        articles_raw = {}
        for item in info:
            item = info[item]
            articles_raw.setdefault(item['pub_date'], [])
            articles_raw[item['pub_date']].append("https://meduza.io/" + item['url'])

        # check if the algorithm reached the date
        date_is_reached = previous_date in articles_raw

        articles_before = merge_articles_data(articles_before, articles_raw)
        i = i + 1

    for article in articles_before:
        one_article = {}
        one_article["date"] = article.replace("-", "/")
        one_article["links"] = articles_before[article]
        articles_urls_list.append(one_article)

    return articles_urls_list


with open("analyze_articles/urls_m.txt", "w") as outfile:
    json.dump(get_articles_since_date(date_raw), outfile)

with open("analyze_articles/urls_m.txt") as json_file:
    urls = json.load(json_file)

urls = sorted(urls, key=lambda k: k['date'])

def get_articles_since_date(links_per_day):
    articles_per_day = []
    try:
        for json_obj in links_per_day:
            article = {}
            article["date"] = json_obj["date"]
            print(json_obj['date'])
            texts = []

            for link in json_obj["links"]:
                text = get_text(link)
                texts.append(text)

            article['texts'] = texts
            articles_per_day.append(article)
            # write_to_file("analyze_articles/texts_meduza.txt", articles_per_day)
    finally:
        write_to_file("analyze_articles/texts_meduza.txt", articles_per_day)

get_articles_since_date(urls)
with open("analyze_articles/texts_meduza.txt") as json_file:
    articles_m = json.load(json_file)

