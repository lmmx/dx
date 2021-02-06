from ....share.scraper.parse_topics import topics
from ....share.scraper.url_utils import base_url
from ....share.scraper.time_utils import StopWatch
from ..data import dir_path as data_dir
import requests
import csv
from time import sleep
from sys import stderr

__all__ = ["StrWrapIterator", "DummyPage", "GET_book_metadata_pages"]

class StrWrapIterator:
    "Wrap an integer iterator (or even a mix of int and str) as str, with no generator"
    def __init__(self, values):
        self.values = list(values)
        self.start = 0
        self.stop = len(self.values)
        self.timer = None # Only create timer using yield value after first iteration
        return

    def __iter__(self):
        return self

    def __next__(self):
        if self.remaining_iterations < 1:
            raise StopIteration
        if isinstance(self.current_value, int):
            current = repr(self.current_value)
        else:
            current = self.current_value
        self.start += 1
        return current

    @property
    def current_value(self):
        return self.values[self.start]

    @property
    def remaining_iterations(self):
        return self.stop - self.start

    @property
    def timer(self):
        return self._timer

    @timer.setter
    def timer(self, stopwatch):
        self._timer = stopwatch # use a StopWatch

    def pause(self):
        if self.timer:
            self.timer.wait()
        return

class DummyPage:
    def __init__(self, url, ok=True):
        self.url = url
        self.ok = ok
        return

    def __repr__(self):
        return f"<url: {self.url}, ok: {self.ok}>"

def GET_book_metadata_pages(initialise_at=1, volumes=None, sort=True, dry_run=False):
    """
    Retrieve book info pages by GET requests to the AMS book store website,
    with a hard-coded crawl delay of 20 as per the site's `robots.txt`.
    """
    series_suffix = "text"
    reprint_suffix = "r"
    with open(data_dir / "book-series-number-listing.csv") as csvfile:
        reader = csv.reader(csvfile)
        series_dict = dict(reader)
    if "NaN" in series_dict:
        series_dict.pop("NaN") # Discard the unusable entries
    if sort:
        series_dict = dict(sorted(series_dict.items(), key=lambda item: int(item[0])))
    if volumes is None:
        volumes = series_dict.keys()
    volume_iterator = StrWrapIterator(volumes) # yield strings only
    if dry_run:
        crawl_delay = 0.1
    else:
        crawl_delay = 20 # https://bookstore.ams.org/robots.txt --> Crawl-delay: 20
        session = requests.Session()
    for k in volume_iterator:
        if int(k) < initialise_at:
            continue
        suffix_list = [series_suffix, k]
        # title-case `true`/`false` then `eval` as bool
        is_reprint = eval(series_dict.get(k).title())
        if is_reprint:
            suffix_list.append(reprint_suffix)
        page_url = base_url + "-".join(suffix_list) + "/"
        if dry_run:
            dummy_page = DummyPage(page_url)
            yielding = dummy_page
        else:
            retrieved_page = session.get(page_url)
            yielding = retrieved_page
        if volume_iterator.remaining_iterations > 0:
            # Set the timer before the next iteration
            volume_iterator.timer = StopWatch(crawl_delay)
        else:
            volume_iterator.timer = None
        yield yielding
        # Then at the next iteration, wait for however long is left on the timer
        if volume_iterator.timer:
            volume_iterator.timer.wait() # Delay after each crawl, obeying robots.txt
