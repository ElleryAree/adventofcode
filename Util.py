def test(expected, actual, name=None, comparator=lambda a, e: a == e):
    if name is None:
        name = ""
    else:
        name = "%s: " % name
    if not comparator(actual, expected):
        print("[x] %sFailed: Expected %s, but was: %s" % (name, expected, actual))
    else:
        print("[*] %sPassed" % name)

def test_is_not_incorrect(expected, actual, name=None):
    if name is None:
        name = ""
    else:
        name = "%s: " % name
    if expected == actual:
        print("[x] %sFailed: %d is not the right value" % (name, expected))
    else:
        print("[*] %sPassed" % name)

def test_is_not_too_big(expected, actual, name=None):
    if name is None:
        name = ""
    else:
        name = "%s: " % name
    if expected <= actual:
        print("[x] %sFailed: %d was too big. Actual was %d" % (name, expected, actual))
    else:
        print("[*] %sPassed" % name)

def test_is_not_too_low(expected, actual, name=None):
    if name is None:
        name = ""
    else:
        name = "%s: " % name
    if expected >= actual:
        print("[x] %sFailed: %d was too low. Actual was %d" % (name, expected, actual))
    else:
        print("[*] %sPassed" % name)


def from_file(filename):
    with open(filename) as f:
        return f.readlines()


def major_adjacent():
    return (-1, 0), (1, 0), (0, -1), (0, 1)


def diagonally_adjacent():
    return (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)
