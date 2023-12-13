from Util import test, from_file


def parse(lines):
    grid = []
    grids = [grid]

    for line in lines:
        line = line.strip()

        if line != '':
            grid.append(line)
            continue

        grid = []
        grids.append(grid)

    return grids


def print_vertical(middle_point, grid, value):
    print("Vertical middle at %d, value: %d" % (middle_point, value))

    reflection_size = min(middle_point, len(grid[0]) - middle_point)
    for line in grid:
        left_before_ref = line[:middle_point - reflection_size] if middle_point > reflection_size else ""
        left_after_ref = line[middle_point - reflection_size:middle_point]
        right_before_ref = line[middle_point:middle_point + reflection_size]
        right_after_ref = line[middle_point + reflection_size:]

        print('\x1b[0;37;39m' + left_before_ref + '\x1b[0m', end="")
        print('\x1b[0;28;40m' + left_after_ref + '\x1b[0m', end=" ")
        print('\x1b[0;28;40m' + right_before_ref + '\x1b[0m', end="")
        print('\x1b[0;37;39m' + right_after_ref + '\x1b[0m')
    print()


def print_horizontal(middle_point, grid, value):
    print("Horizontal middle at %d, value: %d" % (middle_point, value))

    reflection_size = min(middle_point, len(grid) - middle_point)

    left_before_ref = grid[:middle_point - reflection_size] if middle_point > reflection_size else ""
    left_after_ref = grid[middle_point - reflection_size:middle_point]
    right_before_ref = grid[middle_point:middle_point + reflection_size]
    right_after_ref = grid[middle_point + reflection_size:]

    for line in left_before_ref:
        print('\x1b[0;37;39m' + line + '\x1b[0m')
    for line in left_after_ref:
        print('\x1b[0;28;40m' + line + '\x1b[0m')
    print()
    for line in right_before_ref:
        print('\x1b[0;28;40m' + line + '\x1b[0m')
    for line in right_after_ref:
        print('\x1b[0;37;39m' + line + '\x1b[0m')
    print()


def find_vertical(grid):
    for i in range(len(grid[0]) - 1):
        is_middle = check_vertical_middle(grid, i)
        if is_middle:
            middle = i + 1
            value = middle
            # print_vertical(middle, grid, value)
            return value

    return None


def check_vertical_middle(grid, middle):
    misses = []
    for step in range(middle + 1):
        if middle - step < 0 or middle + step + 1 >= len(grid[0]):
            break

        for line in grid:
            if line[middle - step] != line[middle + step + 1]:

                return False
    return True


def find_horizontal(grid):
    for i in range(len(grid) - 1):
        is_middle = check_horizontal_middle(grid, i)
        if is_middle:
            middle = i + 1
            value = 100 * middle
            # print_horizontal(middle, grid, value)
            return value

    return None


def check_horizontal_middle(grid, middle):
    for step in range(middle + 1):
        if middle - step < 0 or middle + step + 1 >= len(grid):
            break

        line = grid[middle - step]
        other = grid[middle + step + 1]

        for i in range(len(line)):
            if line[i] != other[i]:
                return False

    return True


def find_pattern(grid):
    middle = find_vertical(grid)
    if middle is None:
        middle = find_horizontal(grid)
    return middle


def find_patters(grids):
    total = 0
    for grid in grids:
        middle = find_pattern(grid)
        total += middle

    return total


def part_1(lines):
    return find_patters(parse(lines))


def main():
    test(405, part_1(from_file("test_inputs/13_mirrors")))

    # 33100 too low

    test(33122, part_1(from_file("inputs/13_mirrors")))


if __name__ == '__main__':
    main()
