from ..store import dir_path as store_dir
from pickle import dump, load

__all__ = ["retrieve_pickle", "store_as_pickle"]

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

def store_as_pickle(var_to_pickle, pickle_filename, pickle_dir=None):
    """
    Store a pickle, by default (if `pickle_dir` is `None`),
    in the `scraper` directory's sibling `store` directory.
    """
    if pickle_dir is None:
        pickle_dir = store_dir
    with open(pickle_dir / pickle_filename, "wb") as pickle_file:
        dump(var_to_pickle, pickle_file)
    return
