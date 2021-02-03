from .parse_topics import topics

class Topic:
    def __init__(self, topic_code):
        self.code = topic_code
    
    @property
    def fullname(self):
        return topics.get(self.code)
    
    def __repr__(self):
        return f"{self.code} ({self.fullname})"
