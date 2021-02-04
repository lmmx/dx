from .colours import colour_str
from .soup_processor import tags

__all__ = ["pprint_diff_comp"]

def pprint_diff_comp(diff):
    pprintables = []
    for d in diff:
        if d.startswith("-"):
            pprintable = colour_str("red", d)
        elif d.startswith("+"):
            pprintable = colour_str("green", d)
        elif d.startswith("?"):
            pprintable = colour_str("yellow", d)
        else:
            pprintable = d
        pprintables.append(pprintable)
    for d in pprintables:
        print(d)
    return

def diff_soups(s1, s2):
    t1 = tags(s1)
    t2 = tags(s2)
    t1 == t2
    return
