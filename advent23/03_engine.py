from Util import test, from_file, diagonally_adjacent


class EnginePart:
    def __init__(self, digit):
        self.__digit = digit

    def add_digit(self, digit):
        self.__digit += digit

    def get_number(self):
        return int(self.__digit)


def is_number(c):
    return ord('0') <= ord(c) <= ord('9')


def parse(lines):
    grid = []
    parts = []

    for y, line in enumerate(lines):
        line = line.strip()

        grid_line = []
        grid.append(grid_line)

        for x, c in enumerate(line):
            if is_number(c):
                if x > 0 and is_number(line[x - 1]):
                    engine_part = grid_line[x - 1]
                    engine_part.add_digit(c)
                else:
                    engine_part = EnginePart(c)

                grid_line.append(engine_part)
            else:
                if c != '.':
                    parts.append((c, (x, y)))
                grid_line.append(c)

    return grid, parts


def find_all_parts(grid, parts):
    total = 0

    for c, (x, y) in parts:
        numbers = set()

        for dx, dy in diagonally_adjacent():
            x_dx = x + dx
            y_dy = y + dy

            if 0 > y_dy or y_dy > len(grid) or 0 > x_dx or x_dx > len(grid[y_dy]):
                continue

            engine_part = grid[y_dy][x_dx]
            if engine_part == '.':
                continue

            numbers.add(engine_part.get_number())

        total += sum(numbers)

    return total


def find_gear_ratios(grid, parts):
    total = 0

    for c, (x, y) in filter(lambda v: v[0] == '*', parts):
        numbers = set()

        for dx, dy in diagonally_adjacent():
            x_dx = x + dx
            y_dy = y + dy

            if 0 > y_dy or y_dy > len(grid) or 0 > x_dx or x_dx > len(grid[y_dy]):
                continue

            engine_part = grid[y_dy][x_dx]
            if engine_part == '.':
                continue

            numbers.add(engine_part.get_number())

        if len(numbers) != 2:
            continue

        total += numbers.pop() * numbers.pop()

    return total


def run_stuff(lines, f):
    grid, parts = parse(lines)
    return f(grid, parts)


def run():
    print(run_stuff(from_file("inputs/03_engine"), find_gear_ratios))


def main():
    test(4361, run_stuff(from_file("test_inputs/03_engine"), find_all_parts))
    test(530849, run_stuff(from_file("inputs/03_engine"), find_all_parts))

    test(467835, run_stuff(from_file("test_inputs/03_engine"), find_gear_ratios))
    run()


if __name__ == '__main__':
    main()
