import re
from dx.share import add_classprops_to_ns

class RegexMatchable:
    add_classprops_to_ns(["re"], read_only=True)

    @classmethod
    def match(cls, target_str):
        return re.match(cls.re, target_str)

    @classmethod
    def findall(cls, target_str):
        return re.findall(cls.re, target_str)

    @classmethod
    def finditer(cls, target_str):
        return re.finditer(cls.re, target_str)

    @classmethod
    def listmatches(cls, target_str):
        return list(cls.finditer(target_str))

    @classmethod
    def from_target_str(cls, target_str):
        """
        Class constructor: return an instance of whichever class implements this method
        (i.e. whichever class inherits it) if the class regex (the `re` property) has a
        valid match in `target_str` else return `None` if it doesn't match it.

        N.B. assumes the match is a single item (`m[0]`): use `RegexMultiMatchable` if
        it need not be the case for the given class regex (even if it is sometimes!)
        """
        m = cls.match(target_str)
        return m if m is None else cls(m[0])

class RegexMultiMatchable(RegexMatchable):
    @classmethod
    def from_target_str(cls, target_str):
        """
        Class constructor: return an instance of whichever class implements this method
        (i.e. whichever class inherits it) if the class regex (the `re` property) has a
        valid match in `target_str` else return `None` if it doesn't match it.

        N.B. will always return a list of one or more instances if one or more matches
        are made.
        """
        mm = cls.listmatches(target_str)
        return None if mm is [] else [cls(m) for m in mm]

class SymbolGroup(RegexMultiMatchable):
    def __init__(self, val):
        self.matched = val

    _re = r"\S+\[su[b|p]\(+[^\]]+?\)\]"
