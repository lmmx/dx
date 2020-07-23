from bs4.element import NavigableString as NS
from .soup_processor import review_node_tags, tags
from .soup_structure import AMSGSMInfoPage
from pydoc import pager

def listpager(a_list):
    pager("\n".join([i if type(i) is str else repr(i) for i in a_list]))
    return

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
s2_parsed = AMSGSMInfoPage(s2)

s1_toc_entries = s1_parsed.text_info.toc_info.toc_entries
s2_toc_entries = s2_parsed.text_info.toc_info.toc_entries
