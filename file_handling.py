from analyze_articles import util_functions
import json


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
    new = util_functions.merge_articles_data(old, input)
    write_to_file(filename, new)
