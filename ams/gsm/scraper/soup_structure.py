from dx.share import add_props_to_ns, add_classprops_to_ns, props_as_dict
from bs4 import BeautifulSoup

class HTMLSection(object):
    def __init__(self, html_tag):
        self.root = html_tag
        self._set_up_props()

    # Populate namespace of class definition with properties and class properties
    add_props_to_ns(["root"])
    add_classprops_to_ns(["root_selector"])

    def _attr_tups_from_prop_dict(self):
        attr_tuples = []
        for prop_key, (css_sel, sel_all, *callback) in self._prop_dict.items():
            callback = callback if callable(callback) else lambda x: x
            sel_func = self._selAll if sel_all else self._sel
            attr_tuples.extend([(prop_key, callback(sel_func(css_sel)))])
        return attr_tuples

    def _set_up_props(self):
        if hasattr(self, "_prop_dict"):
            # Set up properties on a subclass calling `super().__init__`
            self._set_attrs(self._attr_tups_from_prop_dict())

    def _set_attrs(self, attr_tuple_list):
        for (attr, val) in attr_tuple_list:
            setattr(self, attr, val)

    def _sel(self, css_selector):
        return self.root.select_one(css_selector)

    def _selAll(self, css_selector):
        return self.root.select(css_selector)


class ContentSection(HTMLSection):
    root_selector = "div.productPage div.bounds"

    _prop_dict = {
        "cover_image": ("img#ProductImage", False),
        "bib_info_print_and_elec": ("p.bibInfo", True),
    }


class TextInfoSection(HTMLSection):
    root_selector = "div.t-stacked.col-md-9 div.bounds"
    
    @staticmethod
    def _process_reviews(reviews):
        return reviews

    @staticmethod
    def _process_metadoc(metadoc):
        return metadoc

    @staticmethod
    def _process_toc(toc):
        return toc

    _prop_dict = {
        "title": ("div.productHeader h1", False),
        "authors": ("span.productAuthors em", True),
        "abstract": ("div.title-abstract div.abstract p", False),
        "readership": ("h4.vertArrow + p", False),
        "reviews": ("div.reviewText div.bounds", False, _process_reviews),
        "metadoc": ("div.doctoc div.bounds div", True, _process_metadoc),
        "toc_info": ("div.doctoc div.bounds ul", False, _process_toc)
    }


class AMSGSMInfoPage(BeautifulSoup):
    def __init__(self, soup):
        # Process then discard the soup
        self.metadata = ContentSection.from_soup(soup)
        self.text_info = TextInfoSection.from_soup(soup)

    _properties = ["metadata", "text_info"]
    add_props_to_ns(_properties)
