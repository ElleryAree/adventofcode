from Util import test, from_file


def get_delta(move):
    """
    returns deltas: q, s, r
    """
    if move == "n":
        return 0, 1, -1
    if move == 'ne':
        return 1, 0, -1
    if move == "se":
        return 1, -1, 0
    if move == 's':
        return 0, -1, 1
    if move == 'nw':
        return -1, 1, 0
    if move == "sw":
        return -1, 0, 1


def calculate_distance(e_q, e_s, e_r):
    return int((abs(e_q) + abs(e_s) + abs(e_r)) / 2)


def follow_path(path):
    path = path.strip().split(",")

    max_distance = 0

    q, s, r = 0, 0, 0

    for step in path:
        dq, ds, dr = get_delta(step)
        q += dq
        s += ds
        r += dr

        distance = calculate_distance(q, s, r)
        if distance > max_distance:
            max_distance = distance

    return calculate_distance(q, s, r), max_distance


def part_1(path):
    return follow_path(path)[0]


def part_2(path):
    return follow_path(path)[1]


def main():
    test(3, part_1("ne,ne,ne"))
    test(0, part_1("ne,ne,sw,sw"))
    test(2, part_1("ne,ne,s,s"))
    test(3, part_1("se,sw,se,sw,sw"))

    test(759, part_1(from_file("inputs/11_hexes")[0]))
    print(part_2(from_file("inputs/11_hexes")[0]))


if __name__ == '__main__':
    main()
