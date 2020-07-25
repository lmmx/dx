from pydoc import pager

def listpager(a_list):
    pager("\n".join([i if type(i) is str else repr(i) for i in a_list]))
    return

def process_reviews(reviews):
    return reviews
