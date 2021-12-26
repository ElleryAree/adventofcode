from math import sqrt

from Util import from_file, test


class Line:
    def __init__(self, start_x, start_y, end_x, end_y):
        self.start_x = start_x
        self.end_x = end_x
        self.start_y = start_y
        self.end_y = end_y

    def __str__(self):
        return "%s, %s -> %s, %s" % (self.start_x, self.start_y, self.end_x, self.end_y)


def coord(pair):
    x, y = pair.split(",")
    return int(x), int(y)


def parse_input(input_lines):
    lines = []

    max_x = -1000000
    max_y = max_x

    for line in input_lines:
        start, end = line.strip().split(" -> ")
        start_x, start_y = coord(start)
        end_x, end_y = coord(end)

        if start_x > max_x:
            max_x = start_x
        if end_x > max_x:
            max_x = end_x

        if start_y > max_y:
            max_y = start_y
        if end_y > max_y:
            max_y = end_y

        lines.append(Line(start_x, start_y, end_x, end_y))

    return max_x, max_y, lines


def build_grid(max_x, max_y):
    return [[0 for _ in range(max_x + 1)] for _ in range(max_y + 1)]


def fill_grid(grid, lines):
    intersections = 0

    def update(up_x, up_y):
        grid[up_y][up_x] += 1

        return 1 if grid[up_y][up_x] == 2 else 0

    for line in lines:
        if line.start_x == line.end_x:
            start, end = order_y(line)

            for y in range(start, end + 1):
                intersections += update(line.start_x, y)
        elif line.start_y == line.end_y:
            start, end = order_x(line)

            for x in range(start, end + 1):
                intersections += update(x, line.start_y)
        else:
            length = abs(line.end_x - line.start_x)

            delta_x = 1 if line.start_x < line.end_x else -1
            delta_y = 1 if line.start_y < line.end_y else -1

            x = line.start_x
            y = line.start_y

            for _ in range(length + 1):
                intersections += update(x, y)
                x += delta_x
                y += delta_y

    return intersections


def order_x(line):
    if line.start_x < line.end_x:
        return line.start_x, line.end_x

    return line.end_x, line.start_x


def order_y(line):
    if line.start_y < line.end_y:
        return line.start_y, line.end_y

    return line.end_y, line.start_y


def print_grid(grid):
    for row in grid:
        print("".join(map(lambda cell: '.' if cell == 0 else str(cell), row)))


def do_run(input_lines, should_print=True):
    max_x, max_y, lines = parse_input(input_lines)

    grid = build_grid(max_x, max_y)
    intersections = fill_grid(grid, lines)

    if should_print:
        print_grid(grid)

    return intersections


def run():
    return do_run(from_file("inputs/05_vents"), should_print=False)


def main():
    test(12, do_run(from_file("test_inputs/05_vents")))
    # test(5774, do_run(from_file("inputs/05_vents"), should_print=False))
    print(run())


if __name__ == '__main__':
    main()
