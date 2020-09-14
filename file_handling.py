import json


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


def write_to_file(filename, new):
    with open(filename, "w") as outfile:
        json.dump(new, outfile)


def read_from_file(filename):
    with open(filename) as json_file:
        output = json.load(json_file)
    return output


def add_to_file(filename, input):
    if filename:
        old = read_from_file(filename)
    new = merge_articles_data(old, input)
    write_to_file(filename, new)
