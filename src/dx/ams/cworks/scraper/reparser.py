from ...share.scraper.reparser import reparse
from .pickle_utils import retrieve_pickle, store_as_pickle
from functools import partial

CRAWLED_AND_PARSED_PICKLE = "cworks-1-26_responses_and_parsings.p"

responses_and_parsed = partial(retrieve_pickle, pickle_filename=CRAWLED_AND_PARSED_PICKLE)

reparse = partial(
    reparse, 
    pickle_retrieval_func=retrieve_pickle,
    pickle_storage_func=store_as_pickle,
    pickle_filename=CRAWLED_AND_PARSED_PICKLE
)
