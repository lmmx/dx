from ..ams.gsm.scraper import topics as subjects  # should be moved into ..share
from ..ams.gsm.scraper.reparser import responses_and_parsed as gsm_results
from ..ams.chel.scraper.reparser import responses_and_parsed as chel_results
from ..ams.conm.scraper.reparser import responses_and_parsed as conm_results
from ..ams.stml.scraper.reparser import responses_and_parsed as stml_results
from ..ams.surv.scraper.reparser import responses_and_parsed as surv_results
from ..ams.amstext.scraper.reparser import responses_and_parsed as amstext_results
from ..ams.amsip.scraper.reparser import responses_and_parsed as amsip_results
from ..ams.cworks.scraper.reparser import responses_and_parsed as cworks_results
from ..ams.crmp.scraper.reparser import responses_and_parsed as crmp_results
from ..ams.dimacs.scraper.reparser import responses_and_parsed as dimacs_results
from ..ams.hmath.scraper.reparser import responses_and_parsed as hmath_results
from ..ams.text.scraper.reparser import responses_and_parsed as text_results

import pandas as pd

__all__ = [
    "series_pages",
    "series_df",
    "series_df_dict",
    "gsm_df",
    "chel_df",
    "conm_df",
    "stml_df",
    "surv_df",
    "amstext_df",
    "amsip_df",
    "cworks_df",
    "crmp_df",
    "dimacs_df",
    "hmath_df",
    "text_df",
    "abstracts",
    "readerships",
    "reviews",
    "titles",
    "tocs",
    "series_by_subject",
    "abstracts_by_subject",
    "readerships_by_subject",
    "reviews_by_subject",
    "titles_by_subject",
    #"tocs_by_subject",
]

series_pages = {
    "gsm": gsm_results()[1],
    "chel": chel_results()[1],
    "conm": conm_results()[1],
    "stml": stml_results()[1],
    "surv": surv_results()[1],
    "amstext": amstext_results()[1],
    "amsip": amsip_results()[1],
    "cworks": cworks_results()[1],
    "crmp": crmp_results()[1],
    "dimacs": dimacs_results()[1],
    "hmath": hmath_results()[1],
    "text": text_results()[1],
}


def pages_to_df(parsed_pages, filter_exceptions=True):
    if filter_exceptions:
        parsed_pages = [p for p in parsed_pages if not isinstance(p, Exception)]
    page_df_list = list(map(lambda p: p._df_repr(), parsed_pages))
    return pd.concat(page_df_list).sort_index(axis=1).reset_index(drop=True)


def abs_readers_revs_tocs(df):
    (_, abstracts), (_, readerships), (_, reviews), (_, titles), (_, tocs) = df.loc[
        :, ("abstract", "readership", "reviews", "title", "toc_info")
    ].iteritems()
    return abstracts, readerships, reviews, titles, tocs


def extract_toc_titles(toc):
    if any(
        map(
            lambda e: getattr(e.title, "ch_num")
            if hasattr(e.title, "ch_num")
            else None,
            toc,
        )
    ):
        titles = [*map(lambda e: e.title if e else [], toc)]
    else:
        breakpoint()
        titles = [*map(lambda e: e.title if e else [], toc)]
    return titles


series_df_dict = dict(
    [
        ("gsm", gsm_df := pages_to_df(series_pages.get("gsm"))),
        ("chel", chel_df := pages_to_df(series_pages.get("chel"))),
        ("conm", conm_df := pages_to_df(series_pages.get("conm"))),
        ("stml", stml_df := pages_to_df(series_pages.get("stml"))),
        ("surv", surv_df := pages_to_df(series_pages.get("surv"))),
        ("amstext", amstext_df := pages_to_df(series_pages.get("amstext"))),
        ("amsip", amsip_df := pages_to_df(series_pages.get("amsip"))),
        ("cworks", cworks_df := pages_to_df(series_pages.get("cworks"))),
        ("crmp", crmp_df := pages_to_df(series_pages.get("crmp"))),
        ("dimacs", dimacs_df := pages_to_df(series_pages.get("dimacs"))),
        ("hmath", hmath_df := pages_to_df(series_pages.get("hmath"))),
        ("text", text_df := pages_to_df(series_pages.get("text"))),
    ]
)

abstracts, readerships, reviews, titles, tocs = [], [], [], [], []
for k, df in series_df_dict.items():
    a, s, r, t, c = abs_readers_revs_tocs(df)
    # print(f"{k}: {len(titles)}", end="... ")
    abstracts.extend(a.tolist())
    readerships.extend(s.tolist())
    reviews.extend(r.tolist())
    titles.extend(t.tolist())
    tocs.extend(
        map(lambda t: extract_toc_titles(t.toc_entries) if t else [], c.tolist())
    )
    # print(len(titles))

series_df = pd.concat(
    [
        df.assign(series=pd.Series(k, dtype="category", index=df.index))
        for k, df in series_df_dict.items()
    ]
).reset_index(drop=True)
series_df.series = series_df.series.astype("category")

series_by_subject = {}
for subject_code in subjects:
    series_by_subject[subject_code] = series_df.loc[
        series_df.subject.apply(lambda row: any(s.code == subject_code for s in row))
    ]

abstracts_by_subject, readerships_by_subject, reviews_by_subject, titles_by_subject = [
    {
        subject_code: series_by_subject[subject_code][col].tolist()
        for subject_code in subjects
    }
    for col in ("abstract", "readership", "reviews", "title")
]
