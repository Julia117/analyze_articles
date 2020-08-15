#functions to download links and texts for newspapers

import json
from newspaper import Article
from bs4 import BeautifulSoup
import requests

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


import datetime

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
    if not dict1:
        return dict2

    for key in (dict1.keys() | dict2.keys()):
        result.setdefault(key, [])
        if key in dict1: result[key] += dict1[key]
        if key in dict2: result[key] += dict2[key]

    # TODO: delete ASAP
    temp = {}
    for x in sorted(result.keys()):
        temp[x] = result[x]
    return temp


#articles for one day
def get_links_for_date_kommersant(date_raw):
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

def get_links_for_date_vedomosti(date_raw):
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

#all articles since given date
def get_links_since_date(date_raw, links_for_date_func): ###links_for_date_func = vedomosti/kommersant
    links= {}
    now = datetime.datetime.now()
    while date_raw.strftime("%Y/%m/%d") <= now.strftime("%Y/%m/%d"):
        print(date_raw.strftime("%Y/%m/%d"))
        urls = links_for_date_func(date_raw)
        links[date_raw.strftime("%Y/%m/%d")] = urls
        date_raw += datetime.timedelta(days=1)
    return links


def get_links_since_date_meduza(date_raw):
    previous_date = (date_raw - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    links = {}
    date_is_reached = False
    i = 0

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

        links = merge_articles_data(links, articles_raw)
        i = i + 1
    return links


def get_articles_since_date(all_links, file):
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
        write_to_file(file, articles)
