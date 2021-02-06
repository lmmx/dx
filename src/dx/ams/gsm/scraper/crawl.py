from ....share.scraper.crawl import crawl
from .crawler import GET_book_metadata_pages

crawl = partial(crawl, book_GET_func=GET_book_metadata_pages)
