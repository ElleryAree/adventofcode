from collections import deque

from Util import test, from_file


def read_lines(lines, preamble_size):
    xmas = Xmas(preamble_size)

    for line in lines:
        number = int(line.strip())

        if not xmas.read_number(number):
            return number


def find_group(lines, target):
    sum = 0
    history = deque()

    for i, line in enumerate(lines):
        number = int(line.strip())

        sum += number
        history.append(number)

        while sum > target:
            sum -= history.popleft()

        if sum == target:
            return find_low_and_high(history)


def find_low_and_high(history):
    low = min(history)
    high = max(history)

    return low + high


def part_two(lines, preamble_size):
    number = read_lines(lines, preamble_size)
    return find_group(lines, number)


class Xmas:
    def __init__(self, preamble_size):
        self.__preamble_size = preamble_size
        self.__preamble = set()
        self.__preamble_history = deque(maxlen=preamble_size)

    def __add_to_preamble(self, number):
        if len(self.__preamble) >= self.__preamble_size:
            first = self.__preamble_history[0]
            self.__preamble.remove(first)

        self.__preamble.add(number)
        self.__preamble_history.append(number)

    def __validate(self, number):
        if len(self.__preamble) < self.__preamble_size:
            return True

        for p_number in self.__preamble:
            if (number - p_number) in self.__preamble:
                return True

        return False

    def read_number(self, number):
        if not self.__validate(number):
            return False

        self.__add_to_preamble(number)
        return True


def run():
    return part_two(from_file("inputs/09_xmas"), 25)


if __name__ == '__main__':
    test_input = ["35\n", "20\n", "15\n", "25\n", "47\n", "40\n", "62\n", "55\n", "65\n", "95\n", "102\n", "117\n", "150\n", "182\n", "127\n", "219\n", "299\n", "277\n", "309\n", "576\n"]

    test(127, read_lines(test_input, 5))

    test(62, part_two(test_input, 5))

    print(run())
