import re
from dx.share import add_props_to_ns, add_classprops_to_ns

class TocChapNum(object):
    def __init__(self, ch_num_substr):
        assert ch_num_substr.endswith("."), ValueError("Chapter number is missing '.'")
        self.substr = ch_num_substr # Store the input substring 'internally'
        num = ch_num_substr[:ch_num_substr.find(".")]
        assert num.isnumeric(), ValueError("Chapter number substring is non-numeric")
        self.numeric = int(num)

    add_props_to_ns(["numeric", "substr"])
    _re = r"(\d+\.)+"
    add_classprops_to_ns(["re"], read_only=True)

    @classmethod
    def match_substr(cls, title_str):
        m = re.match(cls.re, title_str)
        return m if m is None else m[0]

class TocTitle(str):
    def __init__(self, t):
        self.title_text = t
        ch_num_str = TocChapNum.match_substr(t)
        self.ch_num = ch_num_str if ch_num_str is None else TocChapNum(ch_num_str)
        title_postnum = None if self.ch_num is None else t[len(self.ch_num.substr):]
        self.ch_title_postnum = title_postnum
        
    def __repr__(self):
        if self.ch_num is None:
            return self.title_text
        else:
            return f"({self.ch_num.substr}){self.ch_title_postnum}"

class TocEntry(object):
    def __init__(self, li_item):
        title = next(li_item.select_one("span.t-toc-title").stripped_strings)
        self.title = TocTitle(title)
        logical_pageno = li_item.select_one("span.t-toc-logical-pageno")
        self.logical_pageno = None if logical_pageno is None else logical_pageno.text
        pageno = li_item.select_one("span.t-toc-pageno")
        self.pageno = None if pageno is None else pageno.text
        self.is_free = li_item.select_one("span.t-toc-range-free") is not None

class TocEntries(list):
    def __init__(self, li_list):
        self.extend([TocEntry(li) for li in li_list])

    @property
    def has_distinct_pagenums(self):
        return any([e.pageno != e.logical_pageno for e in self])

class TocInfo(object):
    def __init__(self, toc_ul):
        self.toc_entries = TocEntries(toc_ul.findChildren("li", recursive=False))
