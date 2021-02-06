import pandas as pd

class Foo(list):
    toc_entries = []

# dummy classes
class AMSGSMInfoPage:
    def _df_repr(self):
        cols = ['abstract', 'readership', 'reviews', 'title', 'toc_info', 'subject']
        return pd.DataFrame.from_dict({k:[Foo()] for k in cols})

ContentSection = TextInfoSection = AMSGSMInfoPage

