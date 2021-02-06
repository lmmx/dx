from .parse_topics import topics
from .url_utils import base_url
from .time_utils import StopWatch
from .soup_processor import soup_from_response
from .soup_structure import AMSBookInfoPage
from sys import stderr
from time import sleep

__all__ = ["crawl"]

def crawl(book_GET_func, initialise_at=1, volumes=None, sort=True, dry_run=False):
    pages = []
    parsed_pages = []
    book_url_iterator = book_GET_func(initialise_at, volumes, sort, dry_run)
    try:
        for page in book_url_iterator:
            url_subpath = page.url[len(base_url)-1:]
            if page.ok:
                #TODO: process the page
                print(f"GET success: '{url_subpath}'", file=stderr)
                pages.append(page)
                # Process the results here!
                if not dry_run:
                    soup = soup_from_response(page)
                    try:
                        parsed = AMSBookInfoPage(soup)
                    except Exception as e:
                        print(f"Caught {type(e).__name__}: '{e}'", file=stderr)
                        parsed = e # Do this so as to append it and store the exception
                    finally:
                        parsed_pages.append(parsed)
            else:
                print(f"GET failure: '{url_subpath}'", file=stderr)
    except KeyboardInterrupt:
        # Graceful early exit
        n_res = len(pages)
        s = "s" if n_res > 1 else ""
        print(f" » » » Crawler killed (got {n_res} page{s})", file=stderr)
    return pages, parsed_pages

def __main__():
    crawl()

if __name__ == "__main__":
    __main__()
