__all__ = ["base_url", "get_url_suffix"]

base_url = "https://bookstore.ams.org/"

def get_url_suffix(url, to_int=False, as_list=False):
    "Decode the URL info as encoded in `.crawler.GET_book_metadata_pages`"
    if len(url) <= len(base_url):
        raise ValueError(f"This URL is too short: {url}")
    url_suffix = url[url.find("-")+1:].rstrip("/")
    suffix_list = url_suffix.split("-")
    if to_int:
        vol_number = int(suffix_list[0])
    if as_list:
        if to_int:
            is_reprint = len(suffix_list) > 1
            return [vol_number, is_reprint]
        else:
            return suffix_list
    else:
        if to_int:
            return vol_number
        else:
            return url_suffix
