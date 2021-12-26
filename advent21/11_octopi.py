import os
from copy import deepcopy

from Util import test

input = [
    [4, 7, 8, 1, 6, 2, 3, 8, 8, 8],
    [1, 7, 8, 4, 1, 5, 6, 1, 1, 4],
    [3, 2, 6, 5, 6, 4, 5, 1, 2, 2],
    [4, 3, 7, 1, 5, 5, 1, 4, 1, 4],
    [3, 3, 7, 7, 1, 5, 4, 8, 8, 6],
    [7, 8, 8, 2, 3, 1, 4, 4, 5, 5],
    [6, 4, 2, 1, 3, 4, 8, 6, 8, 1],
    [7, 1, 7, 5, 4, 2, 4, 2, 8, 7],
    [5, 4, 8, 8, 2, 4, 2, 1, 8, 4],
    [2, 4, 4, 8, 5, 6, 8, 2, 6, 1]
]

test_input = [
    [5, 4, 8, 3, 1, 4, 3, 2, 2, 3],
    [2, 7, 4, 5, 8, 5, 4, 7, 1, 1],
    [5, 2, 6, 4, 5, 5, 6, 1, 7, 3],
    [6, 1, 4, 1, 3, 3, 6, 1, 4, 6],
    [6, 3, 5, 7, 3, 8, 5, 4, 7, 8],
    [4, 1, 6, 7, 5, 2, 4, 6, 4, 5],
    [2, 1, 7, 6, 8, 4, 1, 7, 2, 1],
    [6, 8, 8, 2, 8, 8, 1, 1, 3, 4],
    [4, 8, 4, 6, 8, 4, 8, 5, 5, 4],
    [5, 2, 8, 3, 7, 5, 1, 5, 2, 6],
]


def update_around_flash(x, y, grid):
    width = len(grid[0])
    height = len(grid)

    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1)):
        next_x = dx + x
        next_y = dy + y

        if next_x < 0 or next_x >= width or next_y < 0 or next_y >= height or grid[next_y][next_x] > 9:
            continue

        grid[next_y][next_x] += 1
        if grid[next_y][next_x] > 9:
            yield next_x, next_y


def simulate_flashes(grid):
    flashes = set()
    flash_queue = []

    for y, row in enumerate(grid):
        for x in range(len(row)):
            row[x] += 1
            if row[x] > 9:
                coord = (x, y)
                flashes.add(coord)
                flash_queue.append(coord)

    while len(flash_queue) > 0:
        x, y = flash_queue.pop()
        for next_coord in update_around_flash(x, y, grid):
            if next_coord not in flashes:
                flashes.add(next_coord)
                flash_queue.append(next_coord)

    for x, y in flashes:
        grid[y][x] = 0

    return len(flashes)


def count_flashes(grid, steps):
    count = 0
    for _ in range(steps):
        count += simulate_flashes(grid)

    return count


def find_all_flash(grid):
    steps = 0
    while True:
        steps += 1
        count = simulate_flashes(grid)

        if count == 100:
            return steps


def run():
    return find_all_flash(input)


def main():
    test(1656, count_flashes(test_input, 100))
    test(1713, count_flashes(input, 100))

    test(195, find_all_flash(test_input))
    print(run())


if __name__ == '__main__':
    main()


