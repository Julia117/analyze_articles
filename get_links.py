from analyze_articles import util_functions

from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def get_links_for_date_kommersant(date_raw):
    """
    Get all articles links for one date from kommersant

    Parameters
    ----------
    date_raw : date in datetime.date("%Y/%m/%d") format

    Returns
    -------
    links
        A list with links

    Notes
    -----
    A kommersant archive page needs to be dynamically loaded. We use
    PhantomJS to press "Show more" ("Показать еще") button and wait
    for a page to fully load.

    """
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
    """
    Notes
    -----
    For vedomosti archive page we retrieve urls from an html page.

    """
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


def get_links_for_period(date_raw_list, links_for_date_func):
    """
    Get all articles links for a period of time for kommersant or vedomosti

    Parameters
    ----------
    date_raw_list : list of dates for which we want to download articles
                    dates in datetime.date("%Y/%m/%d") format

    links_for_date_func : a function to use for downloading links
                            for one date (kommersant or vedomosti)
    Returns
    -------
    links
        A dictionary in format {date : list of links}

    """

    links = {}
    for date in date_raw_list:
        print(date.strftime("%Y/%m/%d"))
        urls = links_for_date_func(date)
        links[date.strftime("%Y/%m/%d")] = urls
    return links


def get_links_for_period_meduza(date_raw_list):
    """
    Get all meduza articles links for a period of time

    Parameters
    ----------
    date_raw_list : list of dates for which we want to download articles
                    dates in datetime.date("%Y/%m/%d") format

    Returns
    -------
    links
        A dictionary in format {date : list of links}

    Notes
    -----
    Meduza provides an API for retrieving links. We load archive data
    starting with up-to-date news and 100 articles info per page.
    We stop when the oldest date in the date_raw_list is reached.

    """

    links = {}
    date_is_reached = False
    i = 0

    while not date_is_reached:
        url = "https://meduza.io/api/v3/search?chrono=news&locale=ru&page=" + str(i) + "&per_page=100"
        response = requests.get(url)
        json_data = response.json()
        info = json_data['documents']
        articles = {}

        for item in info:
            item = info[item]
            date = item['pub_date'].replace('-', '/')
            articles.setdefault(date, [])
            date_raw = datetime.strptime(date, "%Y/%m/%d").date()
            if date_raw >= min(date_raw_list):
                if date_raw <= max(date_raw_list) and date_raw in date_raw_list:
                    articles[date].append("https://meduza.io/" + item['url'])
                else:
                    articles.pop(date)
            else:
                articles.pop(date)
                date_is_reached = True

        links = util_functions.merge_articles_data(links, articles)
        i = i + 1
    return links
