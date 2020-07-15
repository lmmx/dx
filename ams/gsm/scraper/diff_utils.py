from .colours import colour_str

__all__ = ["pprint_diff"]

def pprint_diff(diff):
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
