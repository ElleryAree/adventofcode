from heapq import heappop, heappush

from Util import from_file, test


def parse_input(lines):
    return [list(map(int, line.strip())) for line in lines]


def adjust_score(value, tile_x, tile_y):
    value = value + tile_x + tile_y
    if value > 9:
        value -= 9
    return value


def find_path(grid, grid_size):
    def calc_score(v_x, v_y):
        return (goal[0] - v_x) + (goal[1] - v_y)

    width = len(grid[0])
    height = len(grid)

    goal = width - 1, height - 1, grid_size - 1, grid_size - 1
    frontier = [(calc_score(0, 0), 0, (0, 0, 0, 0))]
    visited = set()

    while len(frontier) > 0:
        score, length, coord = heappop(frontier)

        if coord in visited:
            continue

        visited.add(coord)

        if coord == goal:
            return length

        x, y, tile_x, tile_y = coord
        for d_x, d_y in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            next_x = d_x + x
            next_y = d_y + y
            next_tile_x = tile_x
            next_tile_y = tile_y

            if next_x >= width:
                next_x = 0
                next_tile_x += 1

            if next_y >= height:
                next_y = 0
                next_tile_y += 1

            if next_x < 0 or next_y < 0 or next_tile_x >= grid_size or next_tile_y >= grid_size:
                continue

            next_length = length + adjust_score(grid[next_y][next_x], next_tile_x, next_tile_y)
            next_score = next_length + calc_score(next_x, next_y)

            heappush(frontier, (next_score, next_length, (next_x, next_y, next_tile_x, next_tile_y)))


def run_path(lines):
    return find_path(parse_input(lines), 1)


def run_full(lines):
    return find_path(parse_input(lines), 5)


def test_adjust():
    for y in range(5):
        print(" ".join([str(adjust_score(8, x, y)) for x in range(5)]))


def run():
    return run_full(from_file("inputs/15_risk_levels"))


def main():
    test(40, run_path(from_file("test_inputs/15_risk_levels")))
    test(592, run_path(from_file("inputs/15_risk_levels")))

    test(315, run_full(from_file("test_inputs/15_risk_levels")))
    test(2897, run())


if __name__ == '__main__':
    main()

