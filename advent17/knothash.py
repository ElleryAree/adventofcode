def knot_hash(line):
    lengths = list(map(lambda l: int(str(l)), __string_to_lengths(line)))
    lengths.extend([17, 31, 73, 47, 23])

    source = run_hash(256, lengths, 64)
    dense_hash = __denser_hash(source)

    return "".join(dense_hash)


def __string_to_lengths(line):
    return list(map(lambda c: ord(c), line))


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


def __denser_hash(source):
    dense_hash = []

    for i in range(16):
        off = (i * 16)
        xorded = source[off]

        for j in range(1, 16):
            xorded ^= source[off + j]

        dense_hash.append("{0:02x}".format(xorded))

    return dense_hash
