from bs4 import BeautifulSoup as BS
import bs4
from difflib import Differ
from .diff_utils import pprint_diff_comp
from .pickle_utils import retrieve_pickle
from operator import eq, ne

__all__ = ["split_soups", "diff_from_pickle", "diff_paircomp"]

def split_soups(soups):
    split_soups = [s.prettify().splitlines() for s in soups]
    return split_soups

# e.g.:
# html_diff, (s1, s2) = dx.ams.gsm.scraper.diff_from_pickle("gsm_1-3.p")
def diff_from_pickle(pickle_filename, pickle_dir=None, pprint=False):
    """
    Diff the `requests.Response` objects stored in a pickle.
    """
    unpickled = retrieve_pickle(pickle_filename, pickle_dir)
    soups = [BS(r.content, "html.parser") for r in unpickled]
    line_soups = split_soups(soups)
    # do some zip magic
    # https://stackoverflow.com/questions/20693730/difflib-with-more-than-two-file-names
    html_diff = diff_paircomp(*line_soups[:2])
    return html_diff, soups[:2]

def test():
    _, (s1, s2) = diff_from_pickle("gsm_1-3.p")
    for n in s1.children:
        t = type(n)
        if t == bs4.element.Tag:
            print(n.name)
        else:
            print(t.__name__)
    return

def diff_paircomp(s1, s2):
    html_differ = Differ()
    html_diff = list(html_differ.compare(s1, s2))
    return html_diff
