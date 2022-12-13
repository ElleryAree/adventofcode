from Util import test, from_file


class Packet:
    def __init__(self, line):
        self.__name = line
        # self.__value = eval(line)
        self.__value = self.__parse_line(line)

    @staticmethod
    def __parse_line(line):
        pars = []
        curr_array = []
        symbol = ""

        for c in line:
            if c == '[':
                pars.append(curr_array)
                curr_array = []
                continue

            if c == ']':
                if symbol != '':
                    symbol = int(symbol)
                    curr_array.append(symbol)
                    symbol = ""

                arr = curr_array
                curr_array = pars.pop()
                curr_array.append(arr)
                continue

            if c == ',':
                if symbol != '':
                    symbol = int(symbol)
                    curr_array.append(symbol)
                    symbol = ""
                continue

            symbol += c

        return curr_array

    def __check_pair(self, left, right):
        i = 0

        while True:
            if i >= len(left) and i >= len(right):
                return None
            elif i >= len(left):
                return True
            elif i >= len(right):
                return False

            left_item = left[i]
            right_item = right[i]
            i += 1

            if isinstance(left_item, int) and isinstance(right_item, int):
                if left_item < right_item:
                    return True
                elif left_item > right_item:
                    return False
                else:
                    continue

            if isinstance(left_item, int) and isinstance(right_item, list):
                left_item = [left_item]

            if isinstance(left_item, list) and isinstance(right_item, int):
                right_item = [right_item]

            is_ordered = self.__check_pair(left_item, right_item)
            if is_ordered is not None:
                return is_ordered

    def get_name(self):
        return self.__name

    def __lt__(self, other):
        is_ordered = self.__check_pair(self.__value, other.__value)
        return is_ordered or is_ordered is None


class Pair:
    def __init__(self, index, left, right):
        self.__index = index
        self.__left = left
        self.__right = right

    def is_in_correct_order(self):
        return self.__right > self.__left

    def get_index(self):
        return self.__index

    def __str__(self):
        return "%s: %s -> %s" % (self.__index, self.__left, self.__right)


def parse_input(lines):
    pairs = []
    index = 1

    while len(lines) > 0:
        left = lines.pop(0).strip()
        right = lines.pop(0).strip()
        if len(lines) > 0:
            lines.pop(0)

        pairs.append(Pair(index, Packet(left), Packet(right)))
        index += 1

    return pairs


def parse_input_into_list(lines):
    pairs = []

    for line in lines:
        line = line.strip()
        if line == '':
            continue

        pairs.append(Packet(line))

    pairs.append(Packet("[[2]]"))
    pairs.append(Packet("[[6]]"))

    return pairs


def count_ordered(pairs):
    count = 0
    for pair in pairs:
        if pair.is_in_correct_order():
            count += pair.get_index()

    return count


def sort_and_find(pairs):
    count = 1
    for i, pair in enumerate(sorted(pairs)):
        name = pair.get_name()
        if name == "[[2]]" or name == "[[6]]":
            count *= i + 1
    return count


def parse_and_count(lines):
    return count_ordered(parse_input(lines))


def parse_and_sort(lines):
    return sort_and_find(parse_input_into_list(lines))


def run():
    return parse_and_sort(from_file("inputs/13_packets"))


def main():
    test(13, parse_and_count(from_file("test_inputs/13_packets")))
    test(5659, parse_and_count(from_file("inputs/13_packets")))

    test(140, parse_and_sort(from_file("test_inputs/13_packets")))
    print(run())


if __name__ == '__main__':
    main()
