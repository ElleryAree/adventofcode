import re
from collections import deque

from Util import test, from_file


def apply(number, mask):
    mask_1 = int(mask.replace('X', "1"), 2)
    mask_inv = int(mask.replace('X', "0"), 2)
    return (number & mask_1) | mask_inv


class Runtime:
    def __init__(self):
        self.__mask = None
        self.__memory = {}

    def __set_mask(self, mask):
        self.__mask = list(mask)

    def __apply_mask(self, value):
        value = list(("{0:0%db}" % len(self.__mask)).format(value))
        floats = []
        for i, cm in enumerate(self.__mask):
            if cm == '0':
                continue

            if cm == 'X':
                floats.append(i)

            value[i] = cm

        return int("".join(value).replace("X", "0"), 2), floats

    def __update_memory(self, address, value):
        address, floats = self.__apply_mask(address)

        floats.append(-1)
        queue = deque()
        queue.append((floats[0], floats[1:], ()))

        while len(queue) > 0:
            head, tail, options = queue.pop()

            if head >= 0:
                queue.append((tail[0], tail[1:], options + ((head, 0), )))
                queue.append((tail[0], tail[1:], options + ((head, 1), )))
                continue

            next_address = address
            for i, val in options:
                next_address += val * pow(2, 35 - i)

            self.__memory[next_address] = value

    def __count_values(self):
        return sum(self.__memory.values())

    def __run_line(self, line):
        line = line.strip()
        command, value = line.split(" = ")

        if command == 'mask':
            self.__set_mask(value)
            return

        address = int(command[4:-1])
        self.__update_memory(address, int(value))

    def run(self, lines):
        for line in lines:
            self.__run_line(line)

        return self.__count_values()


def run_lines(lines):
    return Runtime().run(lines)


def run():
    return run_lines(from_file("inputs/14_masks"))


if __name__ == '__main__':
    test_input = ["mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X\n", "mem[8] = 11\n", "mem[7] = 101\n", "mem[8] = 0\n"]
    test_input_2 = ["mask = 000000000000000000000000000000X1001X\n", "mem[42] = 100\n", "mask = 00000000000000000000000000000000X0XX\n", "mem[26] = 1\n"]

    # test(208, run(test_input_2))
    # test(14722016054794, run(from_file("inputs/14_masks")))

    print(run())
    # print("3349152119856 is too low")

