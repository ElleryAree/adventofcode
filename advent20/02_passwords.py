from Util import test, from_file
from re import compile

pattern = compile("(\\d*)-(\\d*) ([a-zA-Z]): (.*)")


def parse_lines(lines):
    return map(parse_line, lines)


def parse_line(line):
    match = pattern.match(line)
    if not match:
        return None

    low = match.group(1)
    high = match.group(2)
    char = match.group(3)
    password = match.group(4)

    return Rule(low, high, char, password)


def count_valid(lines, f):
    return len(list(filter(f, parse_lines(lines))))


class Rule:
    def __init__(self, low, high, char, password):
        self.low = int(low)
        self.high = int(high)
        self.char = char
        self.password = password

    def is_valid(self):
        count = 0
        for char in self.password:
            if char == self.char:
                count += 1

        return self.low <= count <= self.high

    def is_valid_2(self):
        first = self.password[self.low - 1]
        second = self.password[self.high - 1]

        return (first == self.char and second != self.char) or (first != self.char and second == self.char)


def run():
    return count_valid(from_file("inputs/02_passwords"), lambda rule: rule.is_valid_2())


if __name__ == '__main__':
    test_input = ["1-3 a: abcde", "1-3 b: cdefg", "2-9 c: ccccccccc"]
    test(2, count_valid(test_input, lambda rule: rule.is_valid()))
    test(1, count_valid(test_input, lambda rule: rule.is_valid_2()))

    print(run())
