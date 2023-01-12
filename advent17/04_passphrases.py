from Util import test, from_file


def part_1(line):
    return line


def part_2(line):
    return list(map(lambda word: "".join(sorted(word)), line))


def validate(line, f):
    phrases = f(line.strip().split())
    return len(set(phrases)) == len(phrases)


def count_phrases(lines, f):
    total = 0
    for line in lines:
        if validate(line, f):
            total += 1
    return total


def main():
    test(True, validate("aa bb cc dd ee", part_1))
    test(False, validate("aa bb cc dd aa", part_1))
    test(True, validate("aa bb cc dd aaa", part_1))

    test(466, count_phrases(from_file("inputs/04_passphrases"), part_1))
    print(count_phrases(from_file("inputs/04_passphrases"), part_2))


if __name__ == '__main__':
    main()
