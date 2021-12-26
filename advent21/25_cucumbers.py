from copy import deepcopy

from Util import test, from_file


def move(lines):
    return move_vertically(move_horizontaly(lines))


def move_horizontaly(lines):
    next_lines = deepcopy(lines)
    count = 0

    for y, line in enumerate(lines):
        for x, cell in enumerate(line):
            if cell != '.':
                continue

            prev_x = x - 1
            if prev_x < 0:
                prev_x = len(line) - 1

            if line[prev_x] == '>':
                next_lines[y][x] = '>'
                next_lines[y][prev_x] = '.'
                count += 1

    return next_lines, count


def move_vertically(state):
    lines, count = state
    next_lines = deepcopy(lines)

    for y, line in enumerate(lines):
        for x, cell in enumerate(line):
            if cell != '.':
                continue

            prev_y = y - 1
            if prev_y < 0:
                prev_y = len(lines) - 1

            if lines[prev_y][x] == 'v':
                next_lines[y][x] = 'v'
                next_lines[prev_y][x] = '.'
                count += 1

    return next_lines, count


def print_lines(lines, step):
    print("At step %s" % step)
    for line in lines:
        print("".join(line))
    print()


def do_moves(lines, steps):
    lines = list(map(list, lines))

    for step in range(steps):
        lines, changes = move(lines)
        print_lines(lines, step + 1)


def do_moves_until_stop(lines):
    lines = list(map(lambda line: list(line.strip()), lines))
    step = 0
    while True:
        step += 1
        lines, changes = move(lines)
        if changes == 0:
            return step


def run():
    return do_moves_until_stop(from_file("inputs/25_cucumbers"))


def main():
    do_moves(["...>>>>>..."], 2)
    do_moves(["..........", ".>v....v..", ".......>..", ".........."],  1)
    do_moves(["...>...", ".......", "......>", "v.....>", "......>", ".......", "..vvv.."], 4)

    test(58, do_moves_until_stop(from_file("test_inputs/25_cucumbers")))
    test(429, run())


if __name__ == '__main__':
    main()
