from Util import test
from advent17.knothash import knot_hash, run_hash


def run_hash_part_1(size, lengths):
    source = run_hash(size, lengths, 1)
    return source[0] * source[1]

def run_hash_part_2(line):
    return knot_hash(line)


def main():
    test(12, run_hash_part_1(5, [3, 4, 1, 5]))
    test(826, run_hash_part_1(256, [120, 93, 0, 90, 5, 80, 129, 74, 1, 165, 204, 255, 254, 2, 50, 113]))

    test("a2582a3a0e66e6e86e3812dcb672a272", run_hash_part_2(""))
    test("33efeb34ea91902bb2f59c9920caa6cd", run_hash_part_2("AoC 2017"))
    test("3efbe78a8d82f29979031a4aa0b16a9d", run_hash_part_2("1,2,3"))
    test("63960835bcdc130f0b66d7ff4f6a5a8e", run_hash_part_2("1,2,4"))

    print(run_hash_part_2("120,93,0,90,5,80,129,74,1,165,204,255,254,2,50,113"))


if __name__ == '__main__':
    main()
