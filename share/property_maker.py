from inspect import currentframe

__all__ = ["add_props_to_ns", "add_classprops_to_ns", "classproperty", "props_as_dict"]

def prop_getsetdel(property_name, prefix="_", read_only=False, deletable=False):
    internal_attr = prefix + property_name
    def prop_getter(internal_attr):
        def getter_func(self):
            return getattr(self, internal_attr)
        return getter_func

    def prop_setter(internal_attr):
        def setter_func(self, val):
            setattr(self, internal_attr, val)
        return setter_func

    def prop_deleter(internal_attr):
        def deleter_func(self):
            delattr(self, internal_attr)
        return deleter_func

    pget = prop_getter(internal_attr)
    pset = prop_setter(internal_attr)
    pdel = prop_deleter(internal_attr)
    if read_only:
        if deletable:
            return pget, None, pdel # Leave pset `None`
        else:
            return tuple([pget])
    else:
        if deletable:
            return pget, pset, pdel # Full house !
        else:
            return pget, pset

def property_maker(property_name, prefix="_", read_only=False, deletable=False):
    pgsd = prop_getsetdel(property_name, prefix, read_only, deletable)
    return property(*pgsd)

def classproperty_maker(property_name, prefix="_", read_only=False, deletable=False):
    pgsd = prop_getsetdel(property_name, prefix, read_only, deletable)
    return classproperty(*pgsd)

def props_as_dict(prop_names, prefix="_", read_only=False, deletable=False):
    l = [(p, property_maker(p, prefix, read_only, deletable)) for p in prop_names]
    return dict(l)

def classprops_as_dict(prop_names, prefix="_", read_only=False, deletable=False):
    l = [(p, classproperty_maker(p, prefix, read_only, deletable)) for p in prop_names]
    return dict(l)

def add_props_to_ns(property_list, prefix="_", read_only=False, deletable=False):
    try:
        frame = currentframe()
        callers_ns = frame.f_back.f_locals
        d = props_as_dict(property_list, prefix, read_only, deletable)
        callers_ns.update(d)
    finally:
        del frame
    return

def add_classprops_to_ns(property_list, prefix="_", read_only=False, deletable=False):
    try:
        frame = currentframe()
        callers_ns = frame.f_back.f_locals
        d = classprops_as_dict(property_list, prefix, read_only, deletable)
        callers_ns.update(d)
    finally:
        del frame
    return

# use within a class definition as:
# add_props_to_ns(["attr1", "attr2"])

# Decorate a class method to get a static method @property,
# if used to access a __private attribute it makes it immutable
class classproperty(property):
    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()
