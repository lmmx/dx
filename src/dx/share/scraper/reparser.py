from .pickle_utils import retrieve_pickle, store_as_pickle
from .soup_processor import soup_from_response
from .soup_structure import AMSBookInfoPage
from sys import stderr
from traceback import print_tb

def reparse(
    pickle_retrieval_func,
    pickle_storage_func,
    pickle_filename,
    overwrite_pickle=False,
):
    """
    Read back in a stored set of pages (the responses the crawler got)
    and then reparse them with the current scraper code (usually after
    you changed a feature in it and want to update the dataset but
    don't want to wait for the crawler to run again).

    Use `overwrite_pickle` with care: first try to run this function
    without changing it (default: False), to ensure the results are good
    else you might lose your pickle.
    """
    pages, parsed_pages = pickle_retrieval_func(pickle_filename)
    reparsed_pages = []
    for i, page in enumerate(pages):
        soup = soup_from_response(page)
        try:
            parsed = AMSBookInfoPage(soup)
        except Exception as e:
            print(f"{i} Caught {type(e).__name__}: '{e}'", file=stderr)
            print()
            print_tb(e.__traceback__)
            print()
            parsed = e # Do this so as to append it and store the exception
        finally:
            reparsed_pages.append(parsed)
    if overwrite_pickle:
        # The `parsed_pages` will be discarded and replaced with `reparsed_pages`
        pickle_storage_func((pages, reparsed_pages), pickle_filename)
    else:
        return pages, parsed_pages, reparsed_pages
