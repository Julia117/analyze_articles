from utility_functions import file_handling
from datetime import timedelta
from datetime import datetime


def date_range(date1, date2):
    """
    Generates a date range from date1 to date2

    Parameters
    ----------
    date1, date2 : dates in datetime.date("%Y/%m/%d") format

    Returns
    -------
    result
        A list of dates

    """
    result = []
    while date1 <= date2:
        result.append(date1)
        date1 = date1 + timedelta(days=1)
    return result


def get_missing_dates(start_date, end_date, file):
    """
    Get list of missing dates between start_date and end_date in file

    Parameters
    ----------
    start_date, end_date : dates in datetime.date("%Y/%m/%d") format

    file : name of the file to check the date in

    Returns
    -------
    result
        A list of dates

    """
    data = file_handling.read_from_file(file)
    return list(set(date_range(start_date, end_date)) - set([datetime.strptime(date, "%Y/%m/%d").date() for date in data.keys()]))


def merge_articles_data(dict1, dict2):
    """
    Merge two dictionaries into one

    Parameters
    ----------
    dict1, dict2 : dictionaries to be merged

    Returns
    -------
    result
        Dictionary that contains data from dict1 and dict2

    """
    result = {}
    if not dict1:
        return dict2

    for key in (dict1.keys() | dict2.keys()):
        result.setdefault(key, [])
        if key in dict1: result[key] += dict1[key]
        if key in dict2: result[key] += dict2[key]

    return result

