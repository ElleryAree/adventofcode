from Util import test, from_file


def find_cell(lines, start_x, start_y, dx, dy):
    cell = '.'

    while cell == '.':
        start_x = dx + start_x
        start_y = dy + start_y

        if start_x < 0 or start_x >= len(lines[0]):
            return '.'

        if start_y < 0 or start_y >= len(lines):
            return '.'

        cell = lines[start_y][start_x]

    return cell


def update(lines):
    next_grid = []

    for y in range(len(lines)):
        next_row = []
        next_grid.append(next_row)
        for x in range(len(lines[0])):
            cell = lines[y][x]

            if cell == '.':
                next_row.append('.')
                continue

            occupied = 0
            for dx, dy in ((-1, -1), (-1, 0), (0, -1), (0, 1), (1, 0), (1, 1), (-1, 1), (1, -1)):
                other_cell = find_cell(lines, x, y, dx, dy)

                if other_cell == '#':
                    occupied += 1

            if cell == 'L' and occupied == 0:
                next_row.append('#')
            elif cell == '#' and occupied >= 5:
                next_row.append('L')
            else:
                next_row.append(cell)

    return next_grid


def print_grid(lines):
    for line in lines:
        print(" ".join(line))
    print()


def deep_equals(lines, old_lines):
    if old_lines is None:
        return False

    for y in range(len(lines)):
        line = lines[y]
        old_line = old_lines[y]

        if line != old_line:
            return False

    return True


def run_lines(lines):
    lines = parse(lines)
    old_lines = None

    while not deep_equals(lines, old_lines):
        old_lines = lines

        lines = update(lines)

    return count_occupied(lines)


def count_occupied(lines):
    occupied_seats = 0

    for line in lines:
        for cell in line:
            if cell == '#':
                occupied_seats += 1

    return occupied_seats


def parse(lines):
    grid = []
    for line in lines:
        line = line.strip()
        row = []
        row.extend(line)
        grid.append(row)

    return grid


def run():
    return run_lines(from_file("inputs/11_seats"))


if __name__ == '__main__':
    test_input = ["L.LL.LL.LL\n",
                  "LLLLLLL.LL\n",
                  "L.L.L..L..\n",
                  "LLLL.LL.LL\n",
                  "L.LL.LL.LL\n",
                  "L.LLLLL.LL\n",
                  "..L.L.....\n",
                  "LLLLLLLLLL\n",
                  "L.LLLLLL.L\n",
                  "L.LLLLL.LL\n"]

    test(26, run_lines(test_input))
    print(run())
