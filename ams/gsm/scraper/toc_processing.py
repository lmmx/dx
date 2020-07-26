from dx.share import add_props_to_ns
from .symbol_formatting import RegexMatchable, SymbolGroup

class TocChapNum(RegexMatchable):
    def __init__(self, ch_num_substr):
        self.substr = ch_num_substr # Store input string (ToC entry title) in a property
        # Complain if the (sub)chapter numbering regex doesn't match the title string
        assert self.match(self.substr), ValueError("No chapter number in this string")
        self.numeric = self.get_numbering_tuple(self.substr)

    add_props_to_ns(["numeric", "substr"])
    _re = r"^(Chapter )?(\d+\.)+" # set inherited read-only `RegexMatchable.re` property

    @classmethod
    def get_numbering_tuple(cls, target_str):
        m = cls.match(target_str)
        if m:
            mg_ch, mg_num = m.groups()
            num_group = m.group()
            if mg_ch:
                num_group = num_group[len(mg_ch):] # left-strip the chapter substring
            num_tup = tuple(n for n in num_group.split(".") if n)
            num_check = all(map(str.isnumeric, num_tup))
            assert num_check, ValueError(f"Non-numeric chapter numbering: {num_tup}")
            return tuple(map(int, num_tup))
        else:
            return m

class TocTitle(str):
    def __init__(self, t):
        self.title_text = t
        ch_num_str = TocChapNum.from_target_str(t)
        self.ch_num = ch_num_str
        title_postnum = None if self.ch_num is None else t[len(self.ch_num.substr):]
        self.ch_title_postnum = title_postnum
        if self.ch_title_postnum is not None:
            ch_symbol_substrings = SymbolGroup.from_target_str(self.ch_title_postnum)
        else:
            ch_symbol_substrings = []
        self.symbol_groups = ch_symbol_substrings # `.formula.parsed.statement`
        
    def __repr__(self):
        if self.ch_num is None:
            return self.title_text
        else:
            return f"({self.ch_num.substr}){self.ch_title_postnum}"

class TocEntry:
    def __init__(self, li_item):
        title = next(li_item.select_one("span.t-toc-title").stripped_strings)
        self.title = TocTitle(title)
        logical_pageno = li_item.select_one("span.t-toc-logical-pageno")
        self.logical_pageno = None if logical_pageno is None else logical_pageno.text
        pageno = li_item.select_one("span.t-toc-pageno")
        self.pageno = None if pageno is None else pageno.text
        self.is_free = li_item.select_one("span.t-toc-range-free") is not None

    def __repr__(self):
        s = f"{self.title!r} --- {self.logical_pageno}"
        if self.logical_pageno != self.pageno:
            s += f" ({self.pageno})"
        if self.is_free:
            s += " (free)"
        return s

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

class TocInfo:
    def __init__(self, toc_ul):
        self.toc_entries = TocEntries(toc_ul.findChildren("li", recursive=False))
