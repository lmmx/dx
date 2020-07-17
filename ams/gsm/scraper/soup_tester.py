from bs4.element import NavigableString as NS
from .soup_processor import review_node_tags, tags

# from dx.ams.gsm.scraper.soup_tester import *

def review_soup_navstrings(soup, ignores=None):
    """
    Step through the `NavigableString`s one by one to get an idea of
    what information they do/don't have. Except for the ignore list,
    about half are just presentational (e.g. padding nonbreaking spaces)
    and half hold information (e.g. list price is in here).
    """
    dd = soup.descendants
    if ignores is None:
        ignores = [
            "\n",
            " ",
            "\n\xa0",
            " "+"\xa0"*3+" ",
            "\n· "
        ]
    all_good_ns = [d for d in dd if type(d) == NS and d not in ignores]
    for t in all_good_ns:
        print(t.parent)
        _ = input()
        print(f" --> That was the parent of '{t}' (NavigableString of length {len(t)})")
        _ = input()
    return dd, ignores, all_good_ns

nodes1, nodes2, s1, s2 = review_node_tags() # loads pickle `gsm_1-3.p` (vol. 1 to 3)
review_soup_navstrings(s1)
