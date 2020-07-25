from dx.share import add_props_to_ns
from more_itertools import chunked

class ReviewEntry:
    def __init__(self, review, reviewer):
        self.review = review
        self.reviewer = reviewer

    def __repr__(self):
        return f"{self.review}\n—{self.reviewer}"

class Reviews(list):
    def __init__(self, subnodes):
        for (review, reviewer) in chunked([p for p in subnodes if p.name], 2):
            review_text = review.text.replace("\n", " ")
            reviewer_n = reviewer.select_one('span[style="font-style:italic"]').text
            e = ReviewEntry(review_text, reviewer_n)
            self.append(e)
