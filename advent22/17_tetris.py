from math import floor

from Util import test, from_file

rocks = [
    ["####"],
    [".#.", "###", ".#."],
    ["..#", "..#", "###"],
    ["#", "#", "#", "#"],
    ["##", "##"]
]


empty_row = set()


def print_cave(highest_point, cave, rock=None, rock_x=None, rock_y=None):
    for y in range(highest_point, -1, -1):
        cave_row = cave.get(y, empty_row)
        print("%4d |" % y, end="")

        for x in range(7):
            if rock is not  None and rock_x <= x < rock_x + len(rock[0]) and rock_y >= y > rock_y - len(rock):
                c = '@' if rock[rock_y - y][x - rock_x] == '#' else "."
                print(c, end="")
            elif x in cave_row:
                print("#", end="")
            else:
                print(".", end="")
        print("| %d" % y)
    print("     +-------+")
    print()


def print_window(start, window):
    print("     .........")

    for y in range(len(window) - 1, -1, -1):
    # for y, row in enumerate(window):
        row = window[y]
        print("%4d |" % (start - (len(window) - y)), end="")
        for x in range(7):
            if x in row:
                print("#", end="")
            else:
                print(".", end="")
        print("| %d" % (start - (len(window) - y)))
    print("     .........")


def print_num_cave(num_cave):
    print("x --> ", end="")
    for x in range(len(num_cave)):
        print("%3d " % x, end="")
    print()

    print("v --> ", end="")
    for i in num_cave:
        print("%3d " % i, end="")
    print()


def print_matches(num_cave, matches):
    matches, window = matches

    match_id = 0
    start, end = matches[match_id]

    print("m --> ", end="")
    for i in range(len(num_cave)):
        if start <= i <= end:
            print("%3d " % num_cave[i], end="")
        else:
            print("    ", end="")

        if i == end:
            if len(matches) == 0:
                break
            start, end = matches.pop(0)
    print()

    print("w --> ", end="")
    for i in range(len(num_cave)):
        if start <= i <= end:
            print("%3d " % window[i - start], end="")
        else:
            print("    ", end="")
    print()


def print_matches_vertically(num_cave, matches, window, hps):
    print("%3s %3s %3s %s %s " % (" ", " ", "w", " ", " "))
    print("%3s %3s %3s %s %s " % (" ", " ", "i", "c", " "))
    print("%3s %3s %3s %s %s " % (" ", "c", "n", "h", "r"))
    print("%3s %3s %3s %s %s " % (" ", "a", "d", "e", "o"))
    print("%3s %3s %3s %s %s " % (" ", "v", "o", "c", "c"))
    print("%3s %3s %3s %s %s " % ("x", "e", "w", "k", "k"))
    print("%3s %3s %3s %s %s " % ("|", "|", "|", "|", "|"))
    print("%3s %3s %3s %s %s " % ("|", "|", "|", "|", "|"))
    print("%3s %3s %3s %s %s " % ("|", "|", "|", "|", "|"))
    print("%3s %3s %3s %s %s " % ("v", "v", "v", "v", "v"))

    matches_id = 0
    start, end = matches[matches_id]

    for x in range(len(num_cave)):
        cave = num_cave[x]
        if start < x <= end:
            match = window[x - start - 1]
            check = " " if cave == match else "X"
        else:
            match = " "
            check = " "

        if x == end:
            matches_id += 1
            if matches_id >= len(matches):
                start = -1
                end = -1
            else:
                start, end = matches[matches_id]

        rock_num = hps.get(x, " ")

        print("%3s %3s %3s %s %s" % (x, cave, match, check, rock_num))


def to_int(line):
    string = ""
    for x in range(7):
        if x in line:
            string += "1"
        else:
            string += "0"
    return int(string, 2)


def cave_to_int(cave, highest_point):
    nums = []
    for y in range(highest_point + 1):
        nums.append(to_int(cave[y]))
    return nums


def check_window(num_cave, window, i):
    if i + len(window) >= len(num_cave):
        return False

    for l in range(len(window)):
        if num_cave[i + l] != window[l]:
            return False
    return True



def find_window(num_cave, start, window):
    matches = []

    for i in range(start, len(num_cave)):
        if check_window(num_cave, window, i):
            matches.append((i - 1, i - 1 + len(window)))

    return matches


def find_same(num_cave, window_size):
    window = []

    for i in range(len(num_cave)):
        if len(window) < window_size:
            window.append(num_cave[i])
            continue

        matches = find_window(num_cave, i + 1, window)
        if len(matches) > 0:
            return matches, window

        window.pop(0)
        window.append(num_cave[i])


def rock_stopped(cave, rock, rock_x, rock_y):
    if rock_y < 0:
        return True

    if rock_x < 0 or rock_x + len(rock[0]) > 7:
        return True

    for i in range(len(rock)):
        cave_row = cave.get(rock_y - i)
        if cave_row is None:
            continue

        for add_x, c in enumerate(rock[i]):
            if c == '.':
                continue

            if rock_x + add_x in cave_row:
                return True

    return False


def add_rock_to_cave(cave, rock, rock_x, rock_y):
    for i, row in enumerate(rock):
        cave_row = cave.get(rock_y - i)
        if cave_row is None:
            cave_row = set()
            cave[rock_y - i] = cave_row

        for add_x, c in enumerate(row):
            if c == '#':
                cave_row.add(rock_x + add_x)


def simulate_rocks(jets_str, blocks, window_size):
    jets_str = jets_str[0].strip()

    rock_id = 0
    jet_id = 0

    jets = list(map(lambda c: -1 if c == '<' else 1, jets_str))

    cave = {}
    highest_point = -1
    removed_lines = 0

    hps = {}

    for rock_num in range(blocks):
        rock = rocks[rock_id]
        rock_x = 2
        rock_y = highest_point + 3 + len(rock)

        while True:
            jet = jets[jet_id]

            jet_id += 1
            if jet_id >= len(jets):
                jet_id = 0

            next_rock_x = rock_x + jet
            if not rock_stopped(cave, rock, next_rock_x, rock_y):
                rock_x = next_rock_x

            if rock_stopped(cave, rock, rock_x, rock_y - 1):
                break

            rock_y -= 1

        add_rock_to_cave(cave, rock, rock_x, rock_y)
        highest_point = max(cave)

        rock_nums_per_hp = hps.get(highest_point)
        if rock_nums_per_hp is None:
            rock_nums_per_hp = []
            hps[highest_point] = rock_nums_per_hp
        rock_nums_per_hp.append(rock_num)

        rock_id += 1
        if rock_id >= len(rocks):
            rock_id = 0

    num_cave = cave_to_int(cave, highest_point)

    matches = find_same(num_cave, window_size)
    if matches is not None:
        matches, window = matches
        print("Window: %s" % window)
        print("matches: %d: %s" % (len(matches), matches))
        # print_matches_vertically(num_cave, matches, window, hps)
        print()

        return highest_point + removed_lines + 1, matches, window, hps
    else:
        return highest_point + removed_lines + 1, None, None, hps


def find_first_rock_num(hps, window_size, start):
    for x in range(start, start + window_size + 1):
        if x in hps:
            return hps[x]


def find_last_rock_num(hps, window_size, end):
    for x in range(end, end - window_size - 1, -1):
        if x in hps:
            return hps[x]


def find_hp_for_rock(hps, rock_in_match):
    for val, rock_nums in hps.items():
        if rock_in_match in rock_nums:
            return val


def simulate_rocks_generated(lines, window_size, sim_size, target_size):
    hp, matches, window, hps =  simulate_rocks(lines, sim_size, window_size)

    start_1, end_1 = matches[0]
    start_1 += 1

    first_hps = min(find_first_rock_num(hps, window_size, start_1))
    last_hps = max(find_last_rock_num(hps, window_size, end_1))

    rocks_per_match = last_hps - first_hps + 1

    rocks_left = target_size - first_hps
    matches_needed = floor(rocks_left / rocks_per_match)

    rocks_after_last_match = first_hps + matches_needed * rocks_per_match - 1 # 2009 -
    hps_after_last_match = start_1 + matches_needed * window_size

    rocks_still_needed = target_size - rocks_after_last_match - 1
    rock_in_match = first_hps + rocks_still_needed

    last_height = find_hp_for_rock(hps, rock_in_match) - start_1

    final_hp = hps_after_last_match + last_height
    return final_hp - 1


def simulate_rocks_simple(jets_str, blocks, window_size=53):
    res = simulate_rocks(jets_str, blocks, window_size)
    return res[0]


def simulate_rocks_test(jets_str, blocks, window_size=53, sim_blocks=310):
    expected = simulate_rocks(jets_str, blocks, window_size)
    actual = simulate_rocks_generated(from_file("test_inputs/17_tetris"), window_size, 310, blocks)

    test(expected[0], actual, "For blocks count %d" % blocks)


def run():
    return simulate_rocks_generated(from_file("inputs/17_tetris"), 2667, 6022, 1000000000000)


def main():
    # test(3068, simulate_rocks_simple(from_file("test_inputs/17_tetris"), 2022))
    # test(3068, simulate_rocks_generated(from_file("test_inputs/17_tetris"), 53, 310, 2022))
    #
    # simulate_rocks_test(from_file("test_inputs/17_tetris"), 1000)
    # simulate_rocks_test(from_file("test_inputs/17_tetris"), 2019)
    # simulate_rocks_test(from_file("test_inputs/17_tetris"), 2020)
    # simulate_rocks_test(from_file("test_inputs/17_tetris"), 2021)
    # simulate_rocks_test(from_file("test_inputs/17_tetris"), 2022)
    # simulate_rocks_test(from_file("test_inputs/17_tetris"), 2023)
    # simulate_rocks_test(from_file("test_inputs/17_tetris"), 3022)

    # test(3068, simulate_rocks(from_file("test_inputs/17_tetris"), 2022))
    # test(3106, simulate_rocks_simple(from_file("inputs/17_tetris"), 6022, 2667)) # 2667

    # test(1514285714288, simulate_rocks_generated(from_file("test_inputs/17_tetris"), 53, 310, 1000000000000))

    # simulate_rocks_test(from_file("inputs/17_tetris"), 7034, 2667, 6022)

    print(run())


if __name__ == '__main__':
    main()
