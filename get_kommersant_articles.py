from bs4 import BeautifulSoup
import requests
import json

from newspaper import Article
def get_articles_urls_for_date(date):
    url = "https://www.kommersant.ru/archive/list/77/2020-05-02"
    html_content = requests.get(url).text
    html_soup = BeautifulSoup(html_content, "lxml")
    urls = []
    # result = html_soup.find_all('article',attrs={"class": "uho"})
    for c in html_soup.find_all('article',attrs={"class": "uho"}):
        content = c.contents[1]
        if ('href' in content.attrs):
            href = content.attrs['href']
            url = ("https://www.kommersant.ru" + href)
            urls.append(url)
    return urls

get_articles_urls_for_date(date_raw)

def get_articles_urls_since_date(date_raw):
    links_per_day = []
    now = datetime.datetime.now()
    while date_raw.strftime("%Y/%m/%d") <= now.strftime("%Y/%m/%d"):
        url = {}
        urls = get_articles_urls_for_date(date_raw)
        url["date"] = date_raw.strftime("%Y/%m/%d")
        url["links"] = urls
        links_per_day.append(url)
        date_raw += datetime.timedelta(days=1)
    return links_per_day

def get_articles_since_date(links_per_day):
    articles_per_day = []
    for json in links_per_day:
        article = {}
        article["date"] = json["date"]
        for link in json["links"]:
            texts = []
            text = get_text(link)
            texts.append(text)
            article['texts'] = texts
        articles_per_day.append(article)
    return articles_per_day


with open("analyze_articles/urls_k.txt", "w") as outfile:
    json.dump(get_articles_urls_since_date(date_raw), outfile)


with open("analyze_articles/urls_k.txt") as json_file:
    urls = json.load(json_file)

with open("analyze_articles/texts_kommersant.txt", "w") as outfile:
    json.dump(get_articles_since_date(urls), outfile)

with open("analyze_articles/texts_kommersant.txt") as json_file:
    articles = json.load(json_file)

get_articles_urls_for_date(date_raw)