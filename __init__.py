from layouter import Layout


_ids = {}
def uid(name=""):
    # generate a unique id by appending a number to the string
    if name not in _ids:
        _ids[name] = 0

    i = "%s_%d" % (name, _ids[name])
    _ids[name] += 1

    return i
