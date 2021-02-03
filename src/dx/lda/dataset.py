from ..ams.gsm.scraper.reparser import responses_and_reparsed
import pandas as pd

__all__ = ["parsed_pages", "gsm_df", "abstracts", "readerships", "reviews", "titles"]

_, parsed_pages = responses_and_reparsed()
page_df_list = list(map(lambda p: p._df_repr(), parsed_pages))
gsm_df = pd.concat(page_df_list).sort_index(axis=1).reset_index(drop=True)

(_, abstracts), (_, readerships), (_, reviews), (_, titles) = gsm_df.loc[
    :, ("abstract", "readership", "reviews", "title")
].iteritems()
