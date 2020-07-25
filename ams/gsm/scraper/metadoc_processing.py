from dx.share import add_props_to_ns

def strip_text(list_of_tags):
    return [tag.text.strip() for tag in list_of_tags]

def strip_multi(parent_tag):
    "Strip the text of multiple `.t-listitem`-selected `span` tags"
    return strip_text(parent_tag.select(".t-listitem"))

def vol_cb(div):
    return div

def pub_date_cb(div):
    # publication month and year
    return div

def copyr_year_cb(div):
    # publication year
    return div

def pp_cb(div):
    # pagecount
    return div

def covertype_cb(div):
    # think these are all hardbacks?
    return div

def isbn_cb(div):
    # ISBN13 code for the print book
    return div

def applied_cb(div):
    # boolean
    return div

def price_cb(div):
    # book price in USD
    return div

metadoc_callbacks = {
    "authors": strip_multi,
    # what happens when one author doesn't have an affiliation but another does?
    "affiliation": strip_multi,
    "volume": vol_cb,
    "publicationmonthyear": pub_date_cb,
    "copyrightyear": copyr_year_cb,
    "pagecount": pp_cb,
    "covertype": covertype_cb,
    "isbn13print": isbn_cb,
    "mscprimary": strip_multi,
    "mscsecondary": strip_multi,
    "appliedmath": applied_cb,
    "subject": strip_multi, # see `.parse_topics.py`
    "printprice1": price_cb,
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
        self.entries = MetaDocEntries(metadoc_div_items) # 48 tags !
        print(f"{len(metadoc_div_items)=}")
        print(f"{len(self.entries)=}")
        print()
