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


def find_middle(grid, size, check_function, smudges):
    for i in range(size - 1):
        is_middle = check_function(grid, i, smudges)
        if is_middle:
            return i + 1

    return None


def find_vertical(grid, smudges):
    return find_middle(grid, len(grid[0]), check_vertical_middle, smudges)


def find_horizontal(grid, smudges):
    return 100 * find_middle(grid, len(grid), check_horizontal_middle, smudges)


def check_vertical_middle(grid, middle, smudges):
    misses = 0
    for step in range(middle + 1):
        if middle - step < 0 or middle + step + 1 >= len(grid[0]):
            break

        for y, line in enumerate(grid):
            if line[middle - step] != line[middle + step + 1]:
                if misses > smudges:
                    return False
                misses += 1

    return misses == smudges


def check_horizontal_middle(grid, middle, smudges):
    misses = 0
    for step in range(middle + 1):
        if middle - step < 0 or middle + step + 1 >= len(grid):
            break

        line = grid[middle - step]
        other = grid[middle + step + 1]

        for i in range(len(line)):
            if line[i] != other[i]:
                if misses >= smudges:
                    return False
                misses += 1
    return misses == smudges


def find_pattern(grid, smudges):
    middle = find_vertical(grid, smudges)
    if middle is None:
        middle = find_horizontal(grid, smudges)

    return middle


def find_patters(grids, smudges):
    total = 0
    for grid in grids:
        middle = find_pattern(grid, smudges)
        total += middle

    return total


def part_1(lines):
    return find_patters(parse(lines), 0)


def part_2(lines):
    return find_patters(parse(lines), 1)


def run():
    print(part_2(from_file("inputs/13_mirrors")))


def main():
    test(405, part_1(from_file("test_inputs/13_mirrors")))
    test(33122, part_1(from_file("inputs/13_mirrors")))

    test(400, part_2(from_file("test_inputs/13_mirrors")))
    run()


if __name__ == '__main__':
    main()
