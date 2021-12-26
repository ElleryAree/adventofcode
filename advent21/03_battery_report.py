from Util import test, from_file


class Accumulator:
    def __init__(self, len):
        self.__stats = [[0, 0] for _ in range(len)]

    def add_bit(self, value, pos):
        if value == "1":
            self.__stats[pos][0] += 1
        else:
            self.__stats[pos][1] += 1

    def number(self):
        gamma = ""
        epsilon = ""

        for ones, zeros in self.__stats:
            if ones > zeros:
                gamma += "1"
                epsilon += "0"
            else:
                gamma += "0"
                epsilon += "1"

        return int(gamma, 2), int(epsilon, 2)


def find_bits(readings):
    acc = Accumulator(len(readings[0].strip()))

    for reading in readings:
        reading = reading.strip()
        for i, bit in enumerate(reading):
            acc.add_bit(bit, i)

    gamma, epsilon = acc.number()

    return gamma * epsilon


def count_ones_and_zeroes(readings, pos):
    ones = 0
    zeroes = 0

    for reading in readings:
        if reading[pos] == '1':
            ones += 1
        else:
            zeroes += 1

    return ones, zeroes


def find_oxygen(readings, comparator):
    digits = len(readings[0].strip())

    for i in range(digits):
        ones, zeroes = count_ones_and_zeroes(readings, i)

        filter_digit = "1" if comparator(ones, zeroes) else "0"
        readings = list(filter(lambda reading: reading[i] == filter_digit, readings))

        if len(readings) == 1:
            return readings[0]


def find_oxygen_and_co2(reading):
    oxygen = find_oxygen(reading, lambda ones, zeros: ones >= zeros)
    co2 = find_oxygen(reading, lambda ones, zeros: ones < zeros)

    oxygen = int(oxygen, 2)
    co2 = int(co2, 2)

    return oxygen * co2


def run():
    return find_oxygen_and_co2(from_file("inputs/03_battery_report"))


def main():
    test_set = "00100", "11110", "10110", "10111", "10101", "01111", "00111", "11100", "10000", "11001", "00010", "01010"
    # test(198, find_bits(test_set))
    # test(775304, find_bits(from_file("inputs/03_battery_report")))

    test(230, find_oxygen_and_co2(test_set))
    print(run())


if __name__ == '__main__':
    main()
