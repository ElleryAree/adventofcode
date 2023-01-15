from Util import test, from_file


def process_garbage(line):
    count = 0
    while len(line) > 0:
        c = line.pop(0)

        if c == '!':
            line.pop(0)
            continue

        if c == '>':
            return count

        count += 1

    return count


def parse_group(line):
    return parse_group_and_garbage(line)[0]


def parse_garbage(line):
    return parse_group_and_garbage(line)[1]


def parse_group_and_garbage(line):
    total = 0
    total_garbage = 0

    level = 0
    line = list(line.strip())

    while len(line) > 0:
        c = line.pop(0)

        if c == '<':
            total_garbage += process_garbage(line)

        if c == "{":
            level += 1

        if c == "}":
            total += level
            level -= 1

    return total, total_garbage


def main():
    test(1, parse_group("{}"))
    test(6, parse_group("{{{}}}"))
    test(5, parse_group("{{},{}}"))
    test(16, parse_group("{{{},{},{{}}}}"))

    test(1, parse_group("{<a>,<a>,<a>,<a>}"))
    test(9, parse_group("{{<ab>},{<ab>},{<ab>},{<ab>}}"))
    test(9, parse_group("{{<!!>},{<!!>},{<!!>},{<!!>}}"))
    test(3, parse_group("{{<a!>},{<a!>},{<a!>},{<ab>}}"))

    test(13154, parse_group(from_file("inputs/09_garbage")[0]))

    test(0, parse_garbage("{<>}"))
    test(17, parse_garbage("{<random characters>}"))
    test(3, parse_garbage("{<<<<>}"))
    test(2, parse_garbage("{<{!>}>}"))
    test(0, parse_garbage("{<!!>}"))
    test(0, parse_garbage("{<!!!>>}"))
    test(10, parse_garbage("""{<{o"i!a,<{i<a>}"""))

    print(parse_garbage(from_file("inputs/09_garbage")[0]))


if __name__ == '__main__':
    main()
