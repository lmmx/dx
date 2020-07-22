from bs4.element import NavigableString as NS
from .soup_processor import review_node_tags, tags
from .soup_structure import AMSGSMInfoPage
from pydoc import pager

def listpager(a_list):
    pager("\n".join([i if type(i) is str else repr(i) for i in a_list]))
    return

# from dx.ams.gsm.scraper.soup_tester import *
# pager("\n".join(list(dir(next(s1.children)))))
# --> compare to output of soup_tester.js

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

def soup_descendant_counts(soup):
    soup_tags = [d.name for d in s1.descendants if d.name is not None]
    uniq_soup_tags = sorted(set([d.name for d in s1.descendants if d.name is not None]))
    soup_tag_counts = dict(map(lambda k: (k, 0), uniq_soup_tags))
    for tag in soup_tags:
        for desc in soup.descendants:
            if desc.name is tag:
                soup_tag_counts[tag] += 1
    return soup_tag_counts

nodes1, nodes2, s1, s2 = review_node_tags() # loads pickle `gsm_1-3.p` (vol. 1 to 3)
s1_parsed = AMSGSMInfoPage(s1)

#review_soup_navstrings(s1)
#s1_tag_counts = soup_descendant_counts(s1)
#
# ('a', 82)
# ('b', 1)
# ('body', 1)
# ('br', 28)
# ('button', 2)
# ('div', 115)
# ('em', 2)
# ('footer', 1)
# ('form', 3)
# ('h1', 2)
# ('h2', 8)
# ('h3', 2)
# ('h4', 3)
# ('head', 1)
# ('hr', 2)
# ('html', 2)
# ('i', 3)
# ('iframe', 1)
# ('img', 6)
# ('input', 9)
# ('label', 2)
# ('li', 58)
# ('link', 14)
# ('meta', 5)
# ('noscript', 1)
# ('option', 4)
# ('p', 27)
# ('script', 33)
# ('select', 1)
# ('span', 268)
# ('strong', 6)
# ('style', 2)
# ('sup', 1)
# ('table', 1)
# ('tbody', 1)
# ('td', 2)
# ('title', 1)
# ('tr', 2)
# ('ul', 18)
