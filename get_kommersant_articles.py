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

get_articles_urls_for_date("date")