from ..ams.gsm.scraper.reparser import responses_and_reparsed as gsm_results
from ..ams.chel.scraper.reparser import responses_and_reparsed as chel_results
#from ..ams.conm.scraper.reparser import responses_and_reparsed as conm_results
from ..ams.stml.scraper.reparser import responses_and_reparsed as stml_results
from ..ams.surv.scraper.reparser import responses_and_reparsed as surv_results
import pandas as pd

__all__ = [
    "parsed_pages",
    "series_df_dict",
    "gsm_df",
    "chel_df",
#    "conm_df",
    "stml_df",
    "surv_df",
    "abstracts",
    "readerships",
    "reviews",
    "titles",
]

series_pages = {
        "gsm": gsm_results()[1],
        "chel": chel_results()[1],
#        "conm": conm_results()[1],
        "stml": stml_results()[1],
        "surv": surv_results()[1],
}

def pages_to_df(parsed_pages, filter_exceptions=True):
    if filter_exceptions:
        parsed_pages = [p for p in parsed_pages if not isinstance(p, Exception)]
    page_df_list = list(map(lambda p: p._df_repr(), parsed_pages))
    return pd.concat(page_df_list).sort_index(axis=1).reset_index(drop=True)

def abs_readers_revs(df):
    (_, abstracts), (_, readerships), (_, reviews), (_, titles) = df.loc[
        :, ("abstract", "readership", "reviews", "title")
    ].iteritems()
    return abstracts, readerships, reviews, titles

series_df_dict = dict([
    ("gsm", gsm_df := pages_to_df(series_pages.get("gsm"))),
    ("chel", chel_df := pages_to_df(series_pages.get("chel"))),
#    ("conm", conm_df := pages_to_df(series_pages.get("conm"))),
    ("stml", stml_df := pages_to_df(series_pages.get("stml"))),
    ("surv", surv_df := pages_to_df(series_pages.get("surv"))),
])

abstracts, readerships, reviews, titles = [], [], [], []
for k, df in series_df_dict.items():
    a, s, r, t = abs_readers_revs(df)
    #print(f"{k}: {len(titles)}", end="... ")
    abstracts.extend(a.tolist())
    readerships.extend(s.tolist())
    reviews.extend(r.tolist())
    titles.extend(t.tolist())
    #print(len(titles))

series_df = pd.concat([df.assign(series=pd.Series(k, dtype="category", index=df.index)) for k, df in series_df_dict.items()]).reset_index(drop=True)
series_df.series = series_df.series.astype("category")
