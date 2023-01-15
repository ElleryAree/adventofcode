from Util import test


def run_hash(size, lengths, iterations):
    source = list(range(size))
    position = 0
    skip = 0

    for _ in range(iterations):
        for length in lengths:
            for i in range(int(length / 2)):
                current_pos = (position + i) % len(source)
                reversed_pos = (position + (length - 1 - i)) % len(source)

                temp = source[current_pos]
                source[current_pos] = source[reversed_pos]
                source[reversed_pos] = temp

            position = (position + length + skip) % len(source)
            skip += 1

    return source


def denser_hash(source):
    dense_hash = []

    for i in range(16):
        off = (i * 16)
        xorded = source[off]

        for j in range(1, 16):
            xorded ^= source[off + j]

        dense_hash.append("{0:02x}".format(xorded))

    return dense_hash


def run_hash_part_1(size, lengths):
    source = run_hash(size, lengths, 1)
    return source[0] * source[1]


def run_hash_part_2(lengths):
    lengths = list(map(lambda l: int(str(l)), lengths))
    lengths.extend([17, 31, 73, 47, 23])

    source = run_hash(256, lengths, 64)
    dense_hash = denser_hash(source)

    return "".join(dense_hash)


def string_to_lengths(line):
    return list(map(lambda c: ord(c), line))


def main():
    test(12, run_hash_part_1(5, [3, 4, 1, 5]))
    test(826, run_hash_part_1(256, [120, 93, 0, 90, 5, 80, 129, 74, 1, 165, 204, 255, 254, 2, 50, 113]))

    test("a2582a3a0e66e6e86e3812dcb672a272", run_hash_part_2([]))
    test("33efeb34ea91902bb2f59c9920caa6cd", run_hash_part_2(string_to_lengths("AoC 2017")))
    test("3efbe78a8d82f29979031a4aa0b16a9d", run_hash_part_2(string_to_lengths("1,2,3")))
    test("63960835bcdc130f0b66d7ff4f6a5a8e", run_hash_part_2(string_to_lengths("1,2,4")))

    print(run_hash_part_2(string_to_lengths("120,93,0,90,5,80,129,74,1,165,204,255,254,2,50,113")))


if __name__ == '__main__':
    main()
