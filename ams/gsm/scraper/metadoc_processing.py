from dx.share import add_props_to_ns
from .process_topics import Topic

def as_bool(bool_str):
    assert bool_str in ["true", "false"], ValueError(f"Got non-bool: {bool_str}")
    return bool_str == "true"

def as_int(int_str):
    assert int_str.isnumeric(), ValueError(f"Got non-integer: {int_str}")
    return int(int_str)

def strip_text(list_of_tags):
    return [tag.text.strip() for tag in list_of_tags]

def strip_uni_listitem(parent_tag):
    "Strip the text of a single `.t-listitem`-selected `span` tag"
    return parent_tag.select_one(".t-listitem").text.strip()

def strip_uni_value(parent_tag):
    "Strip the text of a single `.t-value-*`-selected `span` tag"
    return parent_tag.select_one('span[class*="t-value-"]').text.strip()

def uni_value_bool(parent_tag):
    "Get the boolean value of a single `.t-value-*`-selected `span` tag"
    return as_bool(strip_uni_value(parent_tag))

def uni_value_int(parent_tag):
    "Get the integer value of a single `.t-value-*`-selected `span` tag"
    return as_int(strip_uni_value(parent_tag))

def strip_multi_listitem(parent_tag):
    "Strip the text of multiple `.t-listitem`-selected `span` tags"
    return strip_text(parent_tag.select(".t-listitem"))

def strip_multi_value(parent_tag):
    "Strip the text of multiple `.t-listitem`-selected `span` tags"
    return strip_text(parent_tag.select('span[class*="t-value-"]'))

def sxg_subject_callback(parent_tag):
    processed = strip_multi_listitem(parent_tag)
    return [Topic(p) for p in processed]

metadoc_callbacks = {
    "authors": strip_multi_listitem,
    # what happens when one author doesn't have an affiliation but another does?
    "affiliation": strip_multi_listitem, # (optional)
    "volume": strip_uni_value, # as integer?
    "publicationmonthyear": strip_uni_value,
    "copyrightyear": strip_uni_value, # as integer?
    "pagecount": uni_value_int,
    "covertype": strip_uni_value,
    "isbn13print": strip_uni_value,
    "mscprimary": strip_multi_listitem,
    "mscsecondary": strip_multi_listitem, # (optional)
    "appliedmath": uni_value_bool,
    "subject": sxg_subject_callback, # Topic class using topics from `parse_topics.py`
    "printprice1": strip_uni_value
}

def get_MetaDocEntry(div):
    meta_type = div.attrs.get("class")[-1].split("-")[1]
    if meta_type in metadoc_callbacks:
        # variable number of these per book, should be between 11-13 pieces of info
        cb = metadoc_callbacks.get(meta_type)
        cbd = cb(div)
        return MetaDocEntry(cbd, meta_type)
    else:
        return None

class MetaDocEntry:
    def __init__(self, val, info_type):
        self.value = val
        self.type = info_type

class MetaDocEntries(list):
    def __init__(self, div_list):
        for div in div_list:
            e = get_MetaDocEntry(div)
            if e:
                self.append(e)

class MetaDoc:
    def __init__(self, metadoc_div_items):
        entries = MetaDocEntries(metadoc_div_items) # filter 48 tags
        entry_names = [e.type for e in entries]
        setattr(self, "_meta_types", entry_names)
        for k, v in zip(entry_names, [e.value for e in entries]):
            setattr(self, k, v)
        self._entries = entries
