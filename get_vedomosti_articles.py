from bs4 import BeautifulSoup
import requests
import json

from newspaper import Article

def get_text(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.text


#get urls from Vedomosti archive
def get_articles_urls_for_date(date_raw):
    url = "https://www.vedomosti.ru/archive/" + date_raw.strftime("%Y/%m/%d")
    html_content = requests.get(url).text
    html_soup = BeautifulSoup(html_content, "lxml")

    for c in html_soup.find_all('script'):
        if (c.get('defer') == None) & (c.get('async') == None):
            data = c.contents[0]

            l = data.find('documents')
            data = data[l + 11:]
            r = data.find(']')
            data = data[:r]

            data = data.replace('\t', '').replace('\n', '')
            data = data.replace("id:", "\"id\":")
            data = data.replace("url:", "\"url\":")
            data = data.replace("title:", "\"title\":")
            data = "{\"main\" : [" + data + "]}"

            y = json.loads(data)
            urls = (["https://www.vedomosti.ru" + t["url"] for t in y["main"]])
            return urls


import datetime
date_raw = datetime.date(2020, 6, 5)
date = date_raw.strftime("%Y/%m/%d")


def get_articles_urls_since_date(date_raw):
    links= {}
    now = datetime.datetime.now()
    while date_raw.strftime("%Y/%m/%d") <= now.strftime("%Y/%m/%d"):
        urls = get_articles_urls_for_date(date_raw)
        links[date_raw.strftime("%Y/%m/%d")] = urls
        date_raw += datetime.timedelta(days=1)
    return links


with open("analyze_articles/urls_vedomosti.txt", "w") as outfile:
    json.dump(get_articles_urls_since_date(date_raw), outfile)


with open("analyze_articles/urls_vedomosti.txt") as json_file:
    urls = json.load(json_file)

def write_to_file(filename, new):
    with open(filename, "w") as outfile:
        json.dump(new, outfile)

def get_articles_since_date(all_links):
    articles = {}
    try:
        for date in all_links:
            print(date)
            texts = []

            for link in all_links[date]:
                try:
                    text = get_text(link)
                except:
                    text = "ERROR"
                texts.append(text)

            articles[date] = texts

    finally:
        print(list(articles.keys())[len(articles.keys())-1])
        write_to_file("analyze_articles/texts_vedomosti.txt", articles)


# def get_articles_since_date(links_per_day):
#     articles_per_day = []
#     try:
#         for json_obj in links_per_day:
#             article = {}
#             article["date"] = json_obj["date"]
#             print(json_obj['date'])
#             for link in json_obj["links"]:
#                 texts = []
#                 text = get_text(link)
#                 texts.append(text)
#                 article['texts'] = texts
#             articles_per_day.append(article)
#             write_to_file("analyze_articles/texts_vedomosti.txt", articles_per_day)
#     finally:
#         write_to_file("analyze_articles/texts_vedomosti.txt", article)


get_articles_since_date(urls)

with open("analyze_articles/texts_vedomosti.txt", "w") as outfile:
    json.dump(get_articles_since_date(urls), outfile)

with open("analyze_articles/texts_vedomosti.txt") as json_file:
    articles = json.load(json_file)


