from ..store import dir_path as store_dir
from pickle import load

__all__ = ["retrieve_pickle"]

def retrieve_pickle(pickle_filename, pickle_dir=None):
    """
    Retrieve a stored pickle, by default (if `pickle_dir` is `None`),
    from the `scraper` directory's sibling `store` directory.
    """
    if pickle_dir is None:
        pickle_dir = store_dir
    with open(pickle_dir / pickle_filename, "rb") as pickle_file:
        unpickled = load(pickle_file)
    return unpickled
