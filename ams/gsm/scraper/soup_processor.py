from bs4 import BeautifulSoup as BS
from difflib import Differ
from .diff_utils import pprint_diff
from .pickle_utils import retrieve_pickle

__all__ = ["diff_from_pickle", "diff_soup_pair"]

def diff_from_pickle(pickle_filename, pickle_dir=None):
    """
    Diff the `requests.Response` objects stored in a pickle.
    """
    unpickled = retrieve_pickle(pickle_filename, pickle_dir)
    soups = [BS(r.content, "html.parser").prettify().splitlines() for r in unpickled]
    # do some zip magic
    # https://stackoverflow.com/questions/20693730/difflib-with-more-than-two-file-names
    html_diff = diff_soup_pair(*soups[:2])
    pprint_diff(html_diff)
    return html_diff, soups[:2]

def diff_soup_pair(s1, s2):
    html_differ = Differ()
    html_diff = list(html_differ.compare(s1, s2))
    return html_diff
