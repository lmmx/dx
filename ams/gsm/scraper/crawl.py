from .parse_topics import topics
from .crawler import GET_book_metadata_pages, base_url
from sys import stderr

__all__ = ["crawl"]

def crawl(initialise_at=1, volumes=range(4), sort=True, dry_run=False):
    all_pages = []
    book_url_iterator = GET_book_metadata_pages(initialise_at, volumes, sort, dry_run)
    try:
        for page in book_url_iterator:
            url_subpath = page.url[len(base_url)-1:]
            if page.ok:
                #TODO: process the page
                print(f"GET success: '{url_subpath}'", file=stderr)
                all_pages.append(page)
            else:
                print(f"GET failure: '{url_subpath}'", file=stderr)
    except KeyboardInterrupt:
        # Graceful early exit
        n_res = len(all_pages)
        s = "s" if n_res > 1 else ""
        print(f" » » » Crawler killed (got {n_res} page{s})", file=stderr)
    return all_pages

def __main__():
    crawl()

if __name__ == "__main__":
    __main__()
