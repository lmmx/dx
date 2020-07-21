from inspect import currentframe

__all__ = ["add_props_to_ns", "add_classprops_to_ns", "classproperty", "props_as_dict"]

def prop_getter_setter(property_name, prefix="_", read_only=False):
    internal_attr = prefix + property_name
    def prop_getter(internal_attr):
        def getter_func(self):
            return getattr(self, internal_attr)
        return getter_func

    def prop_setter(internal_attr):
        def setter_func(self, val):
            setattr(self, internal_attr, val)
        return setter_func

    pget = prop_getter(internal_attr)
    pset = prop_setter(internal_attr)
    if read_only:
        return tuple([pget])
    else:
        return pget, pset

def property_maker(property_name, prefix="_", read_only=False):
    return property(*prop_getter_setter(property_name, prefix, read_only))

def classproperty_maker(property_name, prefix="_", read_only=False):
    return classproperty(*prop_getter_setter(property_name, prefix, read_only))

def props_as_dict(prop_names, prefix="_", read_only=False):
    return dict([(p, property_maker(p, prefix, read_only)) for p in prop_names])

def classprops_as_dict(prop_names, prefix="_", read_only=False):
    return dict([(p, classproperty_maker(p, prefix, read_only)) for p in prop_names])

def add_props_to_ns(property_list, prefix="_", read_only=False):
    try:
        frame = currentframe()
        callers_ns = frame.f_back.f_locals
        callers_ns.update(props_as_dict(property_list, prefix, read_only))
    finally:
        del frame
    return

def add_classprops_to_ns(property_list, prefix="_", read_only=False):
    try:
        frame = currentframe()
        callers_ns = frame.f_back.f_locals
        callers_ns.update(classprops_as_dict(property_list, prefix, read_only))
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
