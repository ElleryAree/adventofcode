def test(expected, actual, name=None, comparator=lambda a, e: a == e):
    if name is None:
        name = ""
    else:
        name = "%s: " % name
    if not comparator(actual, expected):
        print("[x] %sFailed: Expected %s, but was: %s" % (name, expected, actual))
    else:
        print("[*] %sPassed" % name)


def from_file(filename):
    with open(filename) as f:
        return f.readlines()
