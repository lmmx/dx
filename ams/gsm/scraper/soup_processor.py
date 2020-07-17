from bs4 import BeautifulSoup as BS
import bs4
from difflib import Differ
from .diff_utils import pprint_diff_comp
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

def reform_html(html_str):
    """
    Fix the errors in the AMS website HTML so it is not malformed.
    """
    reformed_html_str = reform_html_self_closing_p_tags(html_str)
    reformed_html_str = reform_html_dangling_p_end_tag(reformed_html_str)
    reformed_html_str = reform_html_ul_tags(reformed_html_str)
    return reformed_html_str

def reform_html_dangling_p_end_tag(html_str):
    """
    The HTML on AMS's website contains a 'dangling' `p` end tag, i.e. one
    which doesn't match up to any `p` start tag, meaning it is ignored.
    Remove this by matching the jQuery script (which is unique) after two
    comments (which are not themselves unique within the document).

    (Note: This turned out to have no effect)
    """
    bad_tag = "</p>"
    comments = list(map(lambda c: bs4.Comment(c).output_ready(), [
        "template: com/cubchicken/layout/model/PageBlock/html.ftl ",
        "template: com/cubchicken/plugin/base/model/PageBlockFreeHtml/html.ftl "
    ]))
    jquery_matching_str = "jQuery(document).ready(function(){"
    match_longstr = "\n".join([bad_tag, *comments, "<script>", jquery_matching_str])
    # Delete preceding line
    match_i = html_str.find(bytes(match_longstr, encoding="utf-8"))
    reformed_html_str = html_str[:match_i] + html_str[match_i + len(bad_tag + "\n"):]
    return reformed_html_str

def reform_html_ul_tags(html_str):
    """
    The HTML on AMS's website contains one too many `ul` tags, which leads the
    parser to close the top-level `html` tag. This function finds the last `ul`
    tag and deletes the preceding line (therefore also taking out a surplus
    `li` tag, and leaving it with the correct number of `ul` and `li` tags).
    """
    n_open_ul = html_str.count(b"<ul") # may have attributes
    n_close_ul = html_str.count(b"</ul>")
    if n_open_ul == n_close_ul:
        # Expect this never happens as they're all malformed
        return html_str
    if (n_close_ul - n_open_ul) > 1:
        raise NotImplementedError("There are more than one surplus closing ul tags")
    if (n_open_ul - n_close_ul) > 0:
        raise NotImplementedError("Surplus opening rather than closing ul tags!")
    last_close_ul = html_str.rfind(b"</ul>")
    removal_substring = b"</ul></li>\n" # There's also a surplus `li` to remove
    before_last_close_ul = html_str[:last_close_ul]
    including_and_after_last_close_ul = html_str[last_close_ul:]
    if not before_last_close_ul.endswith(removal_substring):
        raise ValueError("The HTML doesn't have the expected `</ul></li>` to remove")
    trimmed_before_last_close_ul = before_last_close_ul[:-len(removal_substring)]
    reformed_html_str = trimmed_before_last_close_ul + including_and_after_last_close_ul
    return reformed_html_str

def reform_html_self_closing_p_tags(html_str):
    """
    The HTML on AMS's website contains two `p` tags, one of which is malformed
    (it is self closing: `<p .../>` but there is a closing tag `</p>` too).
    This function uses a regex equivalent to `sed "s|<p\([^/]*\) />|<p\1>|g"`
    to reform this malformed tag.
    """
    # sed "s|<p\([^/]*\) />|<p\1>|g"
    malformed_p_re = br"<p([^/]*) />"
    reformed_replacement_re = br"<p\1>"
    reformed_html_str = re.sub(malformed_p_re, reformed_replacement_re, html_str)
    return reformed_html_str

# e.g.:
# html_diff, (s1, s2) = dx.ams.gsm.scraper.diff_from_pickle("gsm_1-3.p")
def diff_from_pickle(pickle_filename, pickle_dir=None, pprint=False):
    """
    Diff the `requests.Response` objects stored in a pickle.
    """
    unpickled = retrieve_pickle(pickle_filename, pickle_dir)
    soups = [BS(reform_html(r.content), "html.parser") for r in unpickled]
    line_soups = split_soups(soups)
    # do some zip magic
    # https://stackoverflow.com/questions/20693730/difflib-with-more-than-two-file-names
    # html_diff = diff_paircomp(*line_soups[:2])
    html_diff = None
    return html_diff, soups

def review_node_tags():
    _, (s1, s2, s3) = diff_from_pickle("gsm_1-3.p")
    nodes1 = []
    nodes2 = []
    for nodes, s in ((nodes1, s1), (nodes2, s2)):
        for n in s.children:
            t = type(n)
            if t == bs4.element.Tag:
                print(n.name)
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
    return nodes1, nodes2, s1, s2

def diff_paircomp(s1, s2):
    html_differ = Differ()
    html_diff = list(html_differ.compare(s1, s2))
    return html_diff
