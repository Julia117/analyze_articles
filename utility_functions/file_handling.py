from utility_functions import util_functions
import json


def write_to_file(filename, new):
    """
    Write JSON to file

    Parameters
    ----------
    filename : name of the file to write to
    new : new JSON data to write to file

    """
    with open(filename, "w") as outfile:
        json.dump(new, outfile)


def read_from_file(filename):
    """
    Read JSON from file

    Parameters
    ----------
    filename : name of the file to read from

    Returns
    -------
    output
        Data in dictionary format
    """
    with open(filename) as json_file:
        output = json.load(json_file)
    return output


def add_to_file(filename, input):
    """
    Add JSON date to file

    Parameters
    ----------
    filename : name of the file to write to

    input : new JSON data

    Notes
    -----
    To add new dictionary to an old one we need to merge them

    """

    old = {}
    if filename:
        old = read_from_file(filename)
    new = util_functions.merge_articles_data(old, input)
    write_to_file(filename, new)
