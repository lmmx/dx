from bs4 import BeautifulSoup as BS
import bs4
from difflib import Differ
#from .diff_utils import pprint_diff_comp
from .pickle_utils import retrieve_pickle
from operator import eq, ne
import re

__all__ = ["split_soups", "diff_from_pickle", "diff_paircomp"]

def split_soups(soups):
    split_soups = [s.prettify().splitlines() for s in soups]
    return split_soups

def tags(soup, names=False):
    tt = [s for s in soup.children if type(s) == bs4.element.Tag]
    if names:
        return [t.name for t in tt]
    else:
        return tt

def diff_from_pickle(pickle_filename, pickle_dir=None, pprint=False):
    unpickled = retrieve_pickle(pickle_filename, pickle_dir)
    soups = [soup_from_response(r) for r in unpickled]
    line_soups = split_soups(soups)
    # do some zip magic
    # https://stackoverflow.com/questions/20693730/difflib-with-more-than-two-file-names
    # html_diff = diff_paircomp(*line_soups[:2])
    html_diff = None
    return html_diff, soups

def soup_from_response(response):
    soup = BS(response.content, "html5lib")
    return soup

def review_node_tags():
    _, (s1, s2, s3) = diff_from_pickle("gsm_1-3.p")
    nodes1 = []
    nodes2 = []
    for nodes, s in ((nodes1, s1), (nodes2, s2)):
        for n in s.children:
            t = type(n)
            if t == bs4.element.Tag:
                print(f"{n.name=}")
                nodes.append(n)
            elif t == bs4.element.NavigableString:
                # Discard these newline strings
                continue
            elif t == bs4.element.Comment:
                # Discard these internal Tizra comments
                continue
            else:
                # In testing there were no other types
                continue
    return nodes1, nodes2, s1, s2, s3

def diff_paircomp(s1, s2):
    html_differ = Differ()
    html_diff = list(html_differ.compare(s1, s2))
    return html_diff
