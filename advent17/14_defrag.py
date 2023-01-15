from Util import test
from advent17.knothash import knot_hash


def hash_to_binary(hash_string):
    binary_line = ""
    for c in hash_string:
        binary_line += "{0:04b}".format(int(c, 16))
    return binary_line


def create_hash(line):
    grid = []
    for i in range(128):
        grid.append(hash_to_binary(knot_hash("%s-%d" % (line, i))))
    return grid


def find_region(grid, c, visited):
    frontier = [c]

    while len(frontier) > 0:
        c = frontier.pop()

        if c in visited:
            continue
        visited.add(c)

        x, y = c

        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            x_dx = x + dx
            y_dy = y + dy

            if y_dy < 0 or y_dy >= len(grid) or x_dx < 0 or x_dx >= len(grid[y_dy]):
                continue

            if grid[y_dy][x_dx] == '1':
                frontier.append((x_dx, y_dy))


def part_1(grid_hash):
    count = 0
    for line in grid_hash:
        for c in line:
            if c == '1':
                count += 1
    return count


def part_2(grid):
    count = 0
    visited = set()

    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            key = x, y
            if key in visited or c == '0':
                continue

            find_region(grid, key, visited)
            count += 1

    return count


def main():
    test_hash = create_hash("flqrgnkx")
    actual_hash = create_hash("vbqugkhl")

    test(8108, part_1(test_hash))
    test(8148, part_1(actual_hash))

    test(1242, part_2(test_hash))
    print(part_2(actual_hash))


if __name__ == '__main__':
    main()
