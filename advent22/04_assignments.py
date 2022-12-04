from Util import test, from_file


class Pair:
    def __init__(self, start, end):
        self.__start = start
        self.__end = end

    def __str__(self):
        return "%d -> %d" % (self.__start, self.__end)

    def intersects(self, other):
        return self.__start <= other.__start and self.__end >= other.__end

    def partial_intersects(self, other):
        return other.__start <= self.__end and other.__end >= self.__start


def parse_pair(pair):
    parts = pair.split("-")
    return Pair(int(parts[0]), int(parts[1]))


def parse_input(line):
    line = line.strip()

    pairs = line.split(",")
    first_pair = parse_pair(pairs[0])
    second_pair = parse_pair(pairs[1])

    return first_pair, second_pair


def find_intersects(first_pair, second_pair, intersect_check):
    return intersect_check(first_pair, second_pair) or intersect_check(second_pair, first_pair)


def total_intersects(first_pair, second_pair):
    return first_pair.intersects(second_pair)


def partial_intersects(first_pair, second_pair):
    return first_pair.partial_intersects(second_pair)


def count_intersects(lines, intersect_check):
    count = 0
    for line in lines:
        first, second = parse_input(line)

        if find_intersects(first, second, intersect_check):
            count += 1

    return count


def run():
    return count_intersects(from_file("inputs/04_assignments"), partial_intersects)


def main():
    test(2, count_intersects(from_file("test_inputs/04_assignments"), total_intersects))
    test(550, count_intersects(from_file("inputs/04_assignments"), total_intersects))

    test(4, count_intersects(from_file("test_inputs/04_assignments"), partial_intersects))
    print(run())


if __name__ == '__main__':
    main()
