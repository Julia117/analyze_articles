from analyze_articles import newsparser
from bs4 import BeautifulSoup
import requests
import json

from newspaper import Article

def get_text(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.text

def get_articles_for_date(date):
    url = "https://www.vedomosti.ru/archive/" + date
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
    df_urls = {}
    now = datetime.datetime.now()
    while date_raw.strftime("%Y/%m/%d") <= now.strftime("%Y/%m/%d"):
        urls = get_articles_for_date(date_raw.strftime("%Y/%m/%d"))
        df_urls[date_raw.strftime("%Y/%m/%d")] = urls
        date_raw += datetime.timedelta(days=1)
    return df_urls

#
# with open("analyze_articles/urls.txt", "w") as outfile:
#     json.dump(get_articles_since_date(date_raw), outfile)

with open(("analyze_articles/urls.txt")) as json_file:
    urls = json.load(json_file)

