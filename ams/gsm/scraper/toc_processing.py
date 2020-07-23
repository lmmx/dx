import re
from dx.share import add_props_to_ns, add_classprops_to_ns

class TocChapNum(object):
    def __init__(self, ch_num_substr):
        self.substr = ch_num_substr # Store input string (ToC entry title) in a property
        # Complain if the (sub)chapter numbering regex doesn't match the title string
        assert self.match(self.substr), ValueError("No chapter number in this string")
        self.numeric = self.get_numbering_tuple(self.substr)

    add_props_to_ns(["numeric", "substr"])
    _re = r"^(Chapter )?(\d+\.)+" # accessed via the read-only `TocChapNum.re` property
    add_classprops_to_ns(["re"], read_only=True)

    @classmethod
    def match(cls, target_str):
        return re.match(cls.re, target_str)

    @classmethod
    def get_numbering_tuple(cls, target_str):
        m = cls.match(target_str)
        if m:
            num_group = m.groups()[1]
            num_tup = tuple(n for n in num_group.split(".") if n)
            num_check = all(map(str.isnumeric, num_tup))
            assert num_check, ValueError(f"Non-numeric chapter numbering: {num_tup}")
            return tuple(map(int, num_tup))
        else:
            return m

    @classmethod
    def from_title_str(cls, title_str):
        """
        Class constructor: return a `TocChapNum` instance if a valid number in
        `title_str` else return `None` if the class regex doesn't match it.
        """
        m = cls.match(title_str)
        return m if m is None else cls(m[0])

class TocTitle(str):
    def __init__(self, t):
        self.title_text = t
        ch_num_str = TocChapNum.from_title_str(t)
        self.ch_num = ch_num_str
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


def get_TocEntry_or_TocEntries(li_item):
    li_ch = li_item.findChild()
    if li_ch.name == "ul":
        entry_list = [TocEntry(l) for l in li_ch.findChildren("li", recursive=False)]
    else:
        entry_list = [TocEntry(li_item)]
    return entry_list

class TocEntries(list):
    def __init__(self, li_list):
        for li in li_list:
            self.extend(get_TocEntry_or_TocEntries(li))

    @property
    def has_distinct_pagenums(self):
        return any([e.pageno != e.logical_pageno for e in self])

class TocInfo(object):
    def __init__(self, toc_ul):
        self.toc_entries = TocEntries(toc_ul.findChildren("li", recursive=False))
