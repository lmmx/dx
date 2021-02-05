from dx.share import add_props_to_ns
from itertools import chain
from more_itertools import chunked
from .soup_postprocessing import listpager

class ReviewEntry:
    def __init__(self, review, reviewer):
        self.review = review
        self.reviewer = reviewer

    def __repr__(self):
        return f"{self.review}\n—{self.reviewer}"

def is_reviewer(text):
    return text.startswith("-- ")

def not_noquote(p_tag):
    """
    Helper function to detect the <p quote="noquote"><bf>Praise for the previous
    edition...</bf></p> tags in listcomp in the `Reviews` class __init__ method.
    Returns whether it is not, so the value can be used directly to omit these tags.
    """
    is_nq = "quote" in p_tag.attrs and p_tag.attrs["quote"] == "noquote"
    return not is_nq

def rc_chunker(subnodes):
    # Omit the empty subnodes and the non-tag subnodes by attribute truthiness
    p_subnodes = [p for p in subnodes if p.name and p.contents and not_noquote(p)]
    naive_review_chunker = chunked(p_subnodes, 2)
    confirmed_tups = []
    for i, rev_tup in enumerate(naive_review_chunker):
        review, reviewer = rev_tup
        if is_reviewer(reviewer.text):
            confirmed_tups.append(rev_tup)
        else:
            # remaining nodes not including current iteration of review, reviewer
            cfi = chain.from_iterable
            remaining_nodes = list(cfi([rev_tup, cfi(naive_review_chunker)]))
            current_review = []
            while remaining_nodes:
                n = remaining_nodes.pop(0)
                if current_review and is_reviewer(n.text):
                    new_tup = tuple([current_review, n])
                    confirmed_tups.append(new_tup)
                    current_review = []
                else:
                    current_review.append(n)
            assert not current_review, f"Could not find reviewer for {current_review=}"
            break
    return confirmed_tups

class Reviews(list):
    def __init__(self, subnodes):
        review_reviewer_tups = rc_chunker(subnodes)
        for review, reviewer in review_reviewer_tups:
            if isinstance(review, list):
                review_text = "\n\n".join([r.text for r in review])
            else:
                review_text = review.text
            review_text = review_text.replace("\n", " ")
            reviewer_n_span = reviewer.select_one('span[style="font-style:italic"]')
            if reviewer_n_span:
                reviewer_n = reviewer_n_span.text
            else:
                if not is_reviewer(reviewer.text):
                    naive_rc = list(chunked([p for p in subnodes if p.name], 2))
                    #listpager(naive_rc)
                assert is_reviewer(reviewer.text), ValueError(
                    f"Reviewer name could not be parsed: '{reviewer.text}'")
                reviewer_n = reviewer.text[reviewer.text.find("-- "):]
            e = ReviewEntry(review_text, reviewer_n)
            self.append(e)
