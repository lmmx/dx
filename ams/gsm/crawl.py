from parse_topics import topics
from crawler import GET_book_metadata_pages, base_url
from sys import stderr

all_pages = []
book_url_iterator = GET_book_metadata_pages(volumes=range(4))
for page in book_url_iterator:
    url_subpath = page.url[len(base_url)-1:]
    if page.ok:
        #TODO: process the page
        print(f"GET success: '{url_subpath}'", file=stderr)
        all_pages.append(page)
    else:
        print(f"GET failure: '{url_subpath}'", file=stderr)
