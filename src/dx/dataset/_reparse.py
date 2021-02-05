from ..share import batch_multiprocess
from ..ams import _all_series as ams_series

from functools import partial

__all__ = ["reparse_all_series"]

def reparse_all_series(overwrite_pickles=False):
    """
    Use multiprocessing to run the reparser on (up to) all CPU cores.

    `scraper.reparse` returns `None` if `overwrite_pickle` is True,
    likewise this function will return `None` if `overwrite_pickles` is True.
    
    Be careful overwriting your parsed dataset! Run the reparser for a single
    series before trying this
    """
    reparse_funcs = [
        partial(m.scraper.reparser.reparse, overwrite_pickle=overwrite_pickles)
        for m in ams_series
    ]
    return batch_multiprocess(reparse_funcs)
