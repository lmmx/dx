from ..store import dir_path as store_dir
from ...share.scraper.pickle_utils import retrieve_pickle, store_as_pickle
from functools import partial

__all__ = ["retrieve_pickle", "store_as_pickle"]

retrieve_pickle = partial(retrieve_pickle, pickle_dir=store_dir)
store_as_pickle = partial(store_as_pickle, pickle_dir=store_dir)
