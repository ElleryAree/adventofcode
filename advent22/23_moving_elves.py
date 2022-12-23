from Util import test, from_file


def parse_lines(lines):
    grid = set()
    for y, line in enumerate(lines):
        line = line.strip()
        for x, c in enumerate(line):
            if c == '#':
                grid.add((x, y))

    return grid


directions = ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1))
NORTH = 1
WEST = 3
EAST = 4
SOUTH = 6

def check_north(positions):
    nw = positions[0]
    n = positions[1]
    ne = positions[2]

    if nw and n and ne:
        return directions[NORTH]
    else:
        return None

def check_south(positions):
    sw = positions[5]
    s = positions[6]
    se = positions[7]

    if sw and s and se:
        return directions[SOUTH]
    else:
        return None

def check_west(positions):
    nw = positions[0]
    w = positions[3]
    sw = positions[5]

    if nw and w and sw:
        return directions[WEST]
    else:
        return None

def check_east(positions):
    ne = positions[2]
    e = positions[4]
    se = positions[7]

    if ne and e and se:
        return directions[EAST]
    else:
        return None


rules = {
    0: check_north,
    1: check_south,
    2: check_west,
    3: check_east
}


def can_move(grid, x, y):
    return list(map(lambda d: (x + d[0], y + d[1]) not in grid, directions))


def calculate_moves(grid, rules_order):
    moves = {}
    for (x, y) in grid:
        positions = can_move(grid, x, y)
        if all(positions):
            continue

        next_delta = None
        for rule_id in rules_order:
            rule = rules[rule_id]
            next_delta = rule(positions)
            if next_delta is not None:
                break

        if next_delta is None:
            continue

        dx, dy = next_delta
        next_move = (x + dx, y + dy)
        next_moves = moves.get(next_move)
        if next_moves is None:
            next_moves = []
            moves[next_move] = next_moves

        next_moves.append((x, y))

    return moves


def cycle_rules(rules_order):
    to_last = rules_order[0]
    rules_order[0] = rules_order[1]
    rules_order[1] = rules_order[2]
    rules_order[2] = rules_order[3]
    rules_order[3] = to_last


def move(grid, moves):
    count = 0
    for next_move, elves in moves.items():
        if len(elves) > 1:
            continue

        grid.remove(elves[0])
        grid.add(next_move)
        count += 1

    return count


def game_step(grid, rules_order):
    moves = calculate_moves(grid, rules_order)
    return move(grid, moves)


def find_dimensions(grid):
    min_x = 10000000000
    max_x = -min_x
    min_y = 10000000000
    max_y = -min_y

    for (x, y) in grid:
        if x > max_x:
            max_x = x
        if x < min_x:
            min_x = x
        if y > max_y:
            max_y = y
        if y < min_y:
            min_y = y

    return min_x, max_x, min_y, max_y


def game(lines):
    grid = parse_lines(lines)
    rules_order = [0, 1, 2, 3]

    for step in range(10):
        game_step(grid, rules_order)
        cycle_rules(rules_order)

    min_x, max_x, min_y, max_y = find_dimensions(grid)

    return (max_x - min_x + 1) * (max_y - min_y + 1) - len(grid)


def game_until_stopped(lines):
    grid = parse_lines(lines)
    rules_order = [0, 1, 2, 3]

    steps = 1
    while True:
        moved = game_step(grid, rules_order)
        cycle_rules(rules_order)

        if moved == 0:
            break
        steps += 1

    return steps


def run():
    return game_until_stopped(from_file("inputs/23_moving_elves"))


def main():
    test(110, game(from_file("test_inputs/23_moving_elves")))
    test(4302, game(from_file("inputs/23_moving_elves")))

    test(20, game_until_stopped(from_file("test_inputs/23_moving_elves")))
    print(run())


if __name__ == '__main__':
    main()
