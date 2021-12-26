from Util import test, from_file


def count_trees(grid, dx=3, dy=1):
    x = 0
    y = 0
    count = 0

    while y < len(grid):
        if grid[y][x] == '#':
            count += 1

        y += dy
        x += dx
        if x >= len(grid[0]):
            x -= len(grid[0])

    return count


def count_all_slopes(grid):
    result = 1
    for dx, dy in ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2)):
        trees = count_trees(grid, dx, dy)
        result *= trees

    return result


def run():
    return count_all_slopes(list(map(lambda line: line.strip(), from_file("inputs/03_trees"))))


if __name__ == '__main__':
    test_input = ["..##.......", "#...#...#..", ".#....#..#.", "..#.#...#.#", ".#...##..#.", "..#.##.....", ".#.#.#....#", ".#........#", "#.##...#...", "#...##....#", ".#..#...#.#"]
    test(7, count_trees(test_input))
    test(336, count_all_slopes(test_input))

    print(run())
