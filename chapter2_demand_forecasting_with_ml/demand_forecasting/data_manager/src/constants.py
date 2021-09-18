def constant(f):
    def fset(self, value):
        raise TypeError

    def fget(self):
        return f()

    return property(fget, fset)


class _CONSTANT(object):
    pass


CONSTANT = _CONSTANT()
