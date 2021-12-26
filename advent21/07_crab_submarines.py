from math import ceil, floor
from statistics import mean, median

from Util import test, from_file


def map_input(line):
    return list(map(int, line[0].strip().split(",")))


def find_target(crabs):
    float_target = mean(crabs)

    ceiling_target = ceil(float_target)
    floor_target = floor(float_target)

    diff_ceil = abs(float_target - ceiling_target)
    diff_floor = abs(float_target - floor_target)

    return floor_target if diff_floor < diff_ceil else ceiling_target


def find_crab_positions(crabs):
    target = find_target(crabs)
    count = 0
    for crab in crabs:
        moves = abs(crab - target)
        cost = func(moves)
        count += cost
    return count


def run():
    return find_crab_positions(map_input(from_file("inputs/07_crab_submarines")))


def main():
    test(168, find_crab_positions(map_input(from_file("test_inputs/07_crab_submarines"))))
    print(run())


def func(n):
    return int(0.5 * (n + 1) * n)


def print_sums():
    moves = list(range(1, 13))
    for i in range(len(moves)):
        slice = moves[:i]
        print("%d: for slice %s: %d, func: %d" % (i, slice, sum(slice), func(i)))


if __name__ == '__main__':
    # print_sums()
    main()
