from bs4 import BeautifulSoup
import json
from newspaper import Article

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


import datetime
date_raw = datetime.date(2020, 6, 5)


def get_text(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.text

import requests
from bs4 import BeautifulSoup


def get_text_new(item):
    url = item['link']
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    texts = soup.find_all('p')
    texts_list = []
    for string in texts:
        texts_list.append(string.text)
    result = "".join(texts_list)
    return result.replace("\xa0", " ")

def write_to_file(filename, new):
    with open(filename, "w") as outfile:
        json.dump(new, outfile)


def get_articles_urls_for_date(date_raw):
    url = "https://www.kommersant.ru/archive/list/77/" + date_raw.strftime("%Y-%m-%d")

    driver = webdriver.PhantomJS("/Users/yulialysenko/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs")
    driver.get(url)

    end = False
    while not end:
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.ui_button.lazyload-button')))
            driver.find_element_by_css_selector('.ui_button.lazyload-button').click()
        except:
            end = True

    html_content = driver.page_source
    driver.quit()
    html_soup = BeautifulSoup(html_content, "lxml")

    links = []
    for c in html_soup.find_all(attrs={"class": "archive_result__item_text"}):
        href = c.contents[1].attrs['href']
        url = ("https://www.kommersant.ru" + href)
        links.append(url)
    return links


get_articles_urls_for_date(date_raw)


def get_articles_urls_since_date(date_raw):
    links_per_day = []
    now = datetime.datetime.now()
    while date_raw.strftime("%Y/%m/%d") <= now.strftime("%Y/%m/%d"):
        print(date_raw)
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