import re
from dx.share import add_props_to_ns, add_classprops_to_ns

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
        self.formula = Formula(self.matched.group())

    _re = r"\S+\[su[b|p]\(+[^\]]+?\)\]"
    add_props_to_ns(["matched", "formula"])

class Formula:
    def __init__(self, match_str):
        self.string = match_str
        self.parsed = self.parse() # Turn into a parsed format

    def parse(self):
        return ParsedFormula(self.string)

class ParsedFormula:
    def __init__(self, string):
        self.parse_from_string(string) # set up root

    def parse_from_string(self, string):
        root_node = string.split()
        self.root = root_node
        if string == "(A[sub(2)])[sup(⊥)]":
            self.parsed = parse_formula_tree(string)
        else:
            self.parsed = None # lol

    add_props_to_ns(["root"])

def closer_for(bracket):
    if bracket == "(":
        return ")"
    elif bracket == "[":
        return "]"
    else:
        raise ValueError("Not one of the 2 opening bracket types")

class TokenGroup:
    def __init__(self, input_string):
        sealed_token_sets = []
        closers = []
        openers = list("([")
        active_char_str = ""
        active_opener = None
        for char in input_string:
            awaiting_closer = closers[-1] if active_opener else None
            if awaiting_closer and char == awaiting_closer:
                # Finished with the string so far
                sealed_token_sets.append(active_char_str)
            if char in openers:
                active_opener = char
                closers.append(closer_for(opener))
            self.internal = input_string


def parse_formula_tree(formula_str):
    formula_str = formula_str.replace("(", "(((").replace(")", ")))")
    formula_str = formula_str.replace("[", "[[[").replace("]", "]]]")
    p_split = [x for xs in [x.split("))") for x in formula_str.split("((")] for x in xs]
    p_split = [x for xs in [x.split("[[") for x in p_split] for x in xs]
    p_split = [x for xs in [x.split("]]") for x in p_split] for x in xs]
    p_split_processed = []
    # Stick on 'overhangs' to the end of the previous splits
    for (i, x) in enumerate(p_split):
        if x.startswith("[") or x.startswith("("):
            p_split_processed[i - 1] += x[0]
            p_split_processed.append(x[1:])
        else:
            p_split_processed.append(x)
    open_index = -1
    split_index_path = [] # Keep a record of the 'path' into the split so far
    pane_list = []
    pane_split_list = []
    # A clopenable is an opener to-be-popped along with its associated closing opener
    # e.g. in `(A[sub(2)])[sup(⊥)]`, one of the splits is `)[` in which `)` remains
    # 'clopen' while the open `[` opener reads until its `]` closer. Once the `[`
    # opener has received an index, the 'clopenable' will be assigned to be 'clopen'
    # alongside the closer `]` for that index (i.e. to become closed along with it).
    # I.e. a clopenable is the 'waiting area' until becoming simply clopen.
    clopenables = []
    clopen_dict = {}
    print(p_split_processed)
    for p in p_split_processed:
        print(f"{split_index_path=}")
        opening_h, opening_v = [p.endswith(x) for x in ("(", "[")]
        closing_h, closing_v = [p.startswith(x) for x in (")", "]")]
        if closing_v or closing_h:
            split_closer = p[0]
            p = p[p.find(split_closer)+1:] # `lstrip(split_closer)` but more carefully
            if not (opening_h or opening_v):
                popped_index = split_index_path.pop()
                if popped_index in clopen_dict:
                    # Pop the associated clopen index which has been kept 'waiting'
                    clopen_to_close = clopen_dict.get(popped_index)
                    clo_check = split_index_path[-1] == clopen_to_close
                    assert clo_check, ValueError(f"Expected {clopen_to_close} clopen")
                    split_index_path.pop()
            else:
                # don't pop the split_index_path but make it a 'clopenable'
                # so as to tie its closure to that of the associated closer
                clopenables.append(split_index_path[-1])
        #######################
        if opening_v or opening_h:
            split_opener = p[-1]
            # the last 0 comma-separated values describe the new pane split, omit them
            p = p[:p.rfind(split_opener)] # `rstrip(split_opener)` but more carefully
            panes_csv = [p]
        pane_it = range(len(panes_csv))  # iterator to take 1 CSV at a time
        pane_descs = map(lambda i: panes_csv[i : (i + 1)], pane_it)
        if len(split_index_path) > 0:
            current_split_i = split_index_path[-1]
        else:
            # This only happens if there are no splits i.e. window only has one pane
            current_split_i = None
        for pane_desc_1_tuple in pane_descs:
            pane_info = ",".join(pane_desc_1_tuple)
            pane = Pane(pane_info, parent_split_index=current_split_i)
            pane_list.append(pane)
        if opening_v or opening_h:
            # Increment the split index for the new PaneSplit being opened
            open_index += 1
            if clopenables:
                clopen_index = clopenables.pop()
                clopen_dict.update({open_index: clopen_index})
            if open_index > 0:
                parent_split_index = split_index_path[-1]
            else:
                parent_split_index = None
            split_index_path.append(open_index)
            split_desc_tuple = p.split(",")
            pane_split_info = ",".join(split_desc_tuple)
            ps = Split(pane_split_info, open_index, parent_split_index)
            pane_split_list.append(ps)
    print(f"---> {split_index_path=}")
    pane_tree = Tree(pane_split_list, pane_list)
    return pane_tree

class Pane:
    def __init__(self, info, parent_split_index):
        self.info = info
        self.parent_split_index = parent_split_index

    def __repr__(self):
        return f"Pane: < {self.info=} ~ #{self.parent_split_index=} >"

class Split:
    def __init__(self, info, open_index, split_index):
        self.info = info
        self.open_index = open_index
        self.split_index = split_index

    def __repr__(self):
        return f"Split: < {self.info=} ~ {self.open_index=} ~ #{self.split_index=} >"

class Tree:
    def __init__(self, splits, panes):
        self.splits = splits
        self.panes = panes

    def __repr__(self):
        split_reprs = "\n".join([f"{s!r}" for s in self.splits])
        panes_reprs = "\n".join([f"{p!r}" for p in self.panes])
        return f"{split_reprs}\n\n{panes_reprs}"