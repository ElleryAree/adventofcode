from Util import test, from_file


def count_offset(to_double_c, c):
    c_count = 0
    for missing_c in to_double_c:
        if missing_c > c:
            break
        c_count += 1
    return c_count


def parse(lines, factor):
    v_galaxies = {}
    to_double_y = []
    found_galaxies = []

    for y, line in enumerate(lines):
        h_galaxies = 0
        for x, c in enumerate(line):
            if c != '#':
                continue

            h_galaxies += 1
            v_galaxies[x] = v_galaxies.get(x, 0) + 1
            found_galaxies.append((x, y))

        if h_galaxies == 0:
            to_double_y.append(y)

    to_double_x = []
    for x in range(len(lines[0])):
        if x not in v_galaxies:
            to_double_x.append(x)

    mult = (factor - 1) if factor > 1 else 1

    expanded_found_galaxies = []
    for x, y in found_galaxies:
        x_count = count_offset(to_double_x, x)
        y_count = count_offset(to_double_y, y)

        expanded_found_galaxies.append((x + (x_count * mult), y + (y_count * mult)))

    return expanded_found_galaxies


def find_shortest_path(found_galaxies):
    total = 0

    visited = set()

    for i1, (x1, y1) in enumerate(found_galaxies):
        for i2, (x2, y2) in enumerate(found_galaxies):
            if (x1 == x2 and y1 == y2) or i1 > i2:
                continue

            dist = abs(x1 - x2) + abs(y1 - y2)
            total += dist
            visited.add((x1, y1, x2, y2))

    return total


def part_1(lines):
    return find_shortest_path(parse(lines, 1))


def part_2(lines, factor=1000000):
    return find_shortest_path(parse(lines, factor))


def run():
    print(part_2(from_file("inputs/11_galaxies"), 1000000))


def main():
    test(374, part_1(from_file("test_inputs/11_galaxies")))
    test(9608724, part_1(from_file("inputs/11_galaxies")))

    test(1030, part_2(from_file("test_inputs/11_galaxies"), 10))
    test(8410, part_2(from_file("test_inputs/11_galaxies"), 100))

    run()


if __name__ == '__main__':
    main()
