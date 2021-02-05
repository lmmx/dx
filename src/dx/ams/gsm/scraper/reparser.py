from .parse_topics import topics
from .url_utils import base_url
from .pickle_utils import retrieve_pickle
from .soup_processor import soup_from_response
from .soup_structure import AMSGSMInfoPage
from sys import stderr
from traceback import print_tb

CRAWLED_AND_PARSED_PICKLE = "gsm-1-208_responses_and_parsings.p"

def responses_only(pickle_filename="gsm-1-208_responses.p"):
    responses = retrieve_pickle(pickle_filename)
    return responses

def parsed_w_errors(pickle_filename="gsm-1-208_responses_and_parsings_with_errors.p"):
    responses, parsed_and_errors = retrieve_pickle(pickle_filename)
    return responses, parsed_and_errors

def parsed_errors_only():
    errors = [p for p in parsed_w_errors()[1] if isinstance(p, Exception)]
    return errors

def parsed_error_tracebacks_only(pickle_filename="gsm-1-208_tracebacks.p"):
    tracebacks = retrieve_pickle(pickle_filename)
    return tracebacks

def parsed_errors_with_tb():
    errors_with_tb = parsed_errors_only()
    tracebacks = parsed_error_tracebacks_only()
    for e, tb_str_list in zip(errors_with_tb, tracebacks):
        setattr(e, "__traceback_str_list__", tb_str_list)
    return errors_with_tb

def responses_and_parsed(pickle_filename=CRAWLED_AND_PARSED_PICKLE):
    responses, reparsed = retrieve_pickle(pickle_filename)
    return responses, reparsed

def parsed_and_df(pickle_filename="gsm-1-208_parsings_and_dataframe.p"):
    parsed, dataframe = retrieve_pickle(pickle_filename)
    return parsed, dataframe

def reparse():
    pages, parsed_pages = responses_and_parsed()
    reparsed_pages = []
    for i, page in enumerate(pages):
        soup = soup_from_response(page)
        try:
            parsed = AMSGSMInfoPage(soup)
        except Exception as e:
            print(f"{i} Caught {type(e).__name__}: '{e}'", file=stderr)
            print()
            print_tb(e.__traceback__)
            print()
            parsed = e # Do this so as to append it and store the exception
        finally:
            reparsed_pages.append(parsed)
    return pages, parsed_pages, reparsed_pages
