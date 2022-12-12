from heapq import heappop, heappush

from Util import test, from_file


def parse_grid(lines):
    grid = []
    start = None
    starts = []
    goal = None

    for y, line in enumerate(lines):
        line = line.strip()
        row = []
        grid.append(row)
        for x, c in enumerate(line):
            if c == 'S':
                start = x, y
                c = 'a'
            if c == 'E':
                goal = x, y
                c = 'z'

            if c == 'a':
                starts.append((x, y))

            c = ord(c) - ord('a')
            row.append(c)

    return grid, start, starts, goal


def find_in_grid(grid, start, goals, is_reverse):
    frontier = [(0, start)]
    visited = set()

    while len(frontier) > 0:
        steps, coord = heappop(frontier)

        if coord in visited:
            continue

        if coord in goals:
            return steps

        visited.add(coord)

        x, y = coord

        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            x_dx = x + dx
            y_dy = y + dy

            if y_dy < 0 or y_dy >= len(grid) or x_dx < 0 or x_dx >= len(grid[y_dy]):
                continue

            current_level = grid[y][x]
            next_level = grid[y_dy][x_dx]

            if is_reverse:
                cond = current_level - next_level <= 1
            else:
                cond = next_level - current_level <= 1

            if cond:
                heappush(frontier, (steps + 1, (x_dx, y_dy)))


def is_in_path(x, y, path):
    for x1, y1 in path:
        if x == x1 and y == y1:
            return 'X'
    return None


def find(lines, only_one):
    grid, start, starts, goal = parse_grid(lines)
    if only_one:
        return find_in_grid(grid, start, (goal, ), False)
    else:
        return find_in_grid(grid, goal, starts, True)


def run():
    return find(from_file("inputs/12_no_signal"), False)


def main():
    test(31, find(from_file("test_inputs/12_no_signal"), True))
    test(462, find(from_file("inputs/12_no_signal"), True))

    test(29, find(from_file("test_inputs/12_no_signal"), False))
    print(run())


if __name__ == '__main__':
    main()
