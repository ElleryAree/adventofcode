from Util import test, from_file


def first(line):
    for c in line:
        if ord('0') <= ord(c) <= ord('9'):
            return c

def last(line):
    for c in reversed(line):
        if ord('0') <= ord(c) <= ord('9'):
            return c


def first_with_letters(line):
    for i, c in enumerate(line):
        if ord('0') <= ord(c) <= ord('9'):
            return c

        if c == 'o' and i + 2 < len(line) and line[i + 1] == 'n' and line[i + 2] == 'e':
                return "1"

        if c == 't':
            if i + 2 < len(line) and line[i + 1] == 'w' and line[i + 2] == 'o':
                    return "2"
            if i + 4 < len(line) and line[i + 1] == 'h' and line[i + 2] == 'r' and line[i + 3] == 'e' and line[i + 4] == 'e':
                    return "3"

        if c == 'f' and i + 3 < len(line):
            if line[i + 1] == 'o' and line[i + 2] == 'u' and line[i + 3] == 'r':
                    return "4"
            if line[i + 1] == 'i' and line[i + 2] == 'v' and line[i + 3] == 'e':
                    return "5"

        if c == 's':
            if i + 2 < len(line) and line[i + 1] == 'i' and line[i + 2] == 'x':
                    return "6"
            if i + 4 < len(line) and line[i + 1] == 'e' and line[i + 2] == 'v' and line[i + 3] == 'e' and line[i + 4] == 'n':
                    return "7"

        if c == 'e' and i + 4 < len(line) and line[i + 1] == 'i' and line[i + 2] == 'g' and line[i + 3] == 'h' and line[i + 4] == 't':
                return "8"

        if c == 'n' and i + 3 < len(line) and line[i + 1] == 'i' and line[i + 2] == 'n' and line[i + 3] == 'e':
                return "9"


def last_with_letters(line):
    for i, c in reversed(list(enumerate(line))):
        if ord('0') <= ord(c) <= ord('9'):
            return c

        if c == 'e':
            if i - 2 >= 0 and line[i - 1] == 'n' and line[i - 2] == 'o':
                return "1"
            if i - 4 >= 0 and line[i - 1] == 'e' and line[i - 2] == 'r' and line[i - 3] == 'h' and line[i - 4] == 't':
                    return "3"
            if i - 3 >= 0 and line[i - 1] == 'v' and line[i - 2] == 'i' and line[i - 3] == 'f':
                    return "5"
            if i - 3 >= 0 and line[i - 1] == 'n' and line[i - 2] == 'i' and line[i - 3] == 'n':
                    return "9"

        if c == 'o' and i - 2 >= 0 and line[i - 1] == 'w' and line[i - 2] == 't':
                    return "2"

        if c == 'r' and i - 3 >= 0 and  line[i - 1] == 'u' and line[i - 2] == 'o' and line[i - 3] == 'f':
                    return "4"

        if c == 'x' and  i - 2 >= 0 and line[i - 1] == 'i' and line[i - 2] == 's':
                    return "6"

        if c == 'n' and i - 4 >= 0 and line[i - 1] == 'e' and line[i - 2] == 'v' and line[i - 3] == 'e' and line[i - 4] == 's':
                    return "7"

        if c == 't' and i - 4 >= 0 and line[i - 1] == 'h' and line[i - 2] == 'g' and line[i - 3] == 'i' and line[i - 4] == 'e':
                return "8"


def calibrate(lines, find_first, find_last):
    total = 0
    for line in lines:
        line = line.strip()
        number = find_first(line) + find_last(line)
        total += int(number)
    return total


def run():
    print(calibrate(from_file("inputs/01_trebuchet"), first_with_letters, last_with_letters))

def main():
    test(142, calibrate(from_file("test_inputs/01_trebuchet"), first, last))
    test(281, calibrate(from_file("test_inputs/01_trebuchet_part_2"), first_with_letters, last_with_letters))

    test(53974, calibrate(from_file("inputs/01_trebuchet"), first, last))
    run()


if __name__ == '__main__':
    main()