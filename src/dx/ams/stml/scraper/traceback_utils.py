import traceback as tb

def exc_tb_str(e):
    str_list = tb.format_exception(type(e), e, e.__traceback__)
    return str_list

def print_tb_str_list(exception=None, str_list=None):
    if not str_list:
        str_list = exception.__traceback_str_list__
    for l in str_list:
        print(l, end="")
    return

def make_tb_trie(tb_str_list):
    """
    https://stackoverflow.com/a/11016430/2668831
    """
    root = dict()
    _end = None
    for tb in tb_str_list:
        current_dict = root
        for key in tb:
            current_dict = current_dict.setdefault(key, {})
        current_dict[_end] = _end
    return root
