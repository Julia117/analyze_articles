from analyze_articles import file_handling
from datetime import timedelta
from datetime import datetime


def date_range(date1, date2):
    result = []
    while date1 <= date2:
        result.append(date1)
        date1 = date1 + timedelta(days=1)
    return result


def get_missing_dates(start_date, end_date, file):
    data = file_handling.read_from_file(file)
    return list(set(date_range(start_date, end_date)) - set([datetime.strptime(date, "%Y/%m/%d").date() for date in data.keys()]))


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
