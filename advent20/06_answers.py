from Util import test, from_file
from re import compile


def scan(lines):
    count = 0
    keys = {}
    people = 0

    for line in lines:
        if line == '\n':
            for total in keys.values():
                if total == people:
                    count += 1

            keys = {}
            people = 0
            continue

        people += 1
        for answer in line.strip():
            total = keys.get(answer, 0)
            keys[answer] = total + 1

    return count


def run():
    return scan(from_file("inputs/06_answers"))


if __name__ == '__main__':
    test(6, scan(["abc", "\n", "a", "b", "c", "\n", "ab", "ac", "\n", "a", "a", "a", "a", "\n", "b", "\n"]))
    print(run())
