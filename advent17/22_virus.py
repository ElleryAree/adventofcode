from Util import from_file, test

LEFT = '<'
RIGHT = '>'
UP = '^'
DOWN = 'v'


moves = {
    LEFT: (-1, 0),
    RIGHT: (1, 0),
    UP: (0, -1),
    DOWN: (0, 1)
}

INFECTED = '#'
FLAGGED = 'F'
WEAKENED = 'W'
CLEAN = '.'

def parse_grid(lines):
    grid = {}
    for y, line in enumerate(lines):
        for x, c in enumerate(line.strip()):
            if c == INFECTED:
                grid[(x, y)] = INFECTED
    return grid


def turn_left(direction):
    if direction == LEFT:
        return DOWN
    if direction == DOWN:
        return RIGHT
    if direction == RIGHT:
        return UP
    if direction == UP:
        return LEFT


def turn_right(direction):
    if direction == LEFT:
        return UP
    if direction == UP:
        return RIGHT
    if direction == RIGHT:
        return DOWN
    if direction == DOWN:
        return LEFT


def reverse(direction):
    if direction == LEFT:
        return RIGHT
    if direction == RIGHT:
        return LEFT
    if direction == UP:
        return DOWN
    if direction == DOWN:
        return UP


def iteration_part_1(grid, x, y, direction):
    coord = (x, y)
    cell = grid.get(coord, CLEAN)

    if cell == INFECTED:
        next_direction = turn_right(direction)
        del grid[coord]
        infected = 0
    else:
        next_direction = turn_left(direction)
        grid[coord] = INFECTED
        infected = 1

    dx, dy = moves[next_direction]

    return x + dx, y + dy, next_direction, infected


def iteration_part_2(grid, x, y, direction):
    coord = (x, y)
    cell = grid.get(coord, CLEAN)

    if cell == INFECTED:
        next_direction = turn_right(direction)
        grid[coord] = FLAGGED
        infected = 0

    elif cell == FLAGGED:
        next_direction = reverse(direction)
        del grid[coord]
        infected = 0

    elif cell == WEAKENED:
        next_direction = direction
        grid[coord] = INFECTED
        infected = 1

    else:
        next_direction = turn_left(direction)
        grid[coord] = WEAKENED
        infected = 0

    dx, dy = moves[next_direction]

    return x + dx, y + dy, next_direction, infected


def run_steps(steps, iteration, lines):
    grid = parse_grid(lines)

    x, y = int((len(lines[0]) - 1) / 2), int(len(lines) / 2)
    direction = UP

    total = 0

    for step in range(steps):
        x, y, direction, infected = iteration(grid, x, y, direction)
        total += infected

    return total


def main():
    test(5587, run_steps(10000, iteration_part_1, from_file("test_inputs/22_virus")))
    test(5240, run_steps(10000, iteration_part_1, from_file("inputs/22_virus")))

    test(26, run_steps(100, iteration_part_2, from_file("test_inputs/22_virus")))
    test(2511944, run_steps(10000000, iteration_part_2, from_file("test_inputs/22_virus")))

    print(run_steps(10000000, iteration_part_2, from_file("inputs/22_virus")))


if __name__ == '__main__':
    main()
