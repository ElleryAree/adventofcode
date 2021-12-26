from Util import test, from_file


class Basin:
    def __init__(self):
        self.count = 0

    def __lt__(self, other):
        return self.count >= other.count

    def __str__(self):
        return str(self.count)


def parse_grid(lines):
    return [list(map(int, line.strip())) for line in lines]


def find_low_point(grid):
    width = len(grid[0])
    height = len(grid)

    count = 0

    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            top = grid[y - 1][x] if y >= 1 else 10
            bottom = grid[y + 1][x] if y < height - 1 else 10
            left = grid[y][x - 1] if x >= 1 else 10
            right = grid[y][x + 1] if x < width - 1 else 10

            if cell < top and cell < bottom and cell < left and cell < right:
                count += cell + 1

    return count


def fill_basin(grid, basin_grid, x, y, basin, width, height):
    stack = [(x, y)]

    while len(stack) > 0:
        x, y = stack.pop()

        if basin_grid[y][x] is not None:
            continue

        if grid[y][x] == 9:
            continue

        basin_grid[y][x] = basin
        basin.count += 1

        for d_x, d_y in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            next_x = x + d_x
            next_y = y + d_y

            if next_x < 0 or next_x >= width or next_y < 0 or next_y >= height:
                continue

            stack.append((next_x, next_y))


def find_basin(grid):
    width = len(grid[0])
    height = len(grid)

    basin_grid = [[None for _ in range(width)] for _ in range(height)]

    basins = []

    for y in range(height):
        for x in range(width):
            if basin_grid[y][x] is not None:
                continue

            basin = Basin()
            basins.append(basin)
            fill_basin(grid, basin_grid, x, y, basin, width, height)

    sorted_basins = list(map(lambda b: b.count, sorted(basins)))

    count = 1
    for basin_size in sorted_basins[:3]:
        count *= basin_size

    return count


def do_count(action, lines):
    return action(parse_grid(lines))


def run():
    return do_count(find_basin, from_file("inputs/09_lava_tubes"))


def main():
    test(15, do_count(find_low_point, from_file("test_inputs/09_lava_tubes")))
    print(do_count(find_low_point, from_file("inputs/09_lava_tubes")))

    test(1134, do_count(find_basin, from_file("test_inputs/09_lava_tubes")))
    print(run())


if __name__ == '__main__':
    main()
