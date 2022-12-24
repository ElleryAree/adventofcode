from Util import test, from_file


test_side_map = {
        (2, 3): 1,
        (2, 2): 2,
        (1, 0): 3,
        (1, 2): 4,
        (0, 2): 5,
        (1, 1): 6
    }

act_side_map = {
    (3, 0): 1,
    (2, 1): 2,
    (2, 0): 3,
    (0, 2): 4,
    (0, 1): 5,
    (1, 1): 6
}

test_transitions = {
    (1, 0): (5, 2, lambda lx, ly, size: size - 1, lambda lx, ly, size: size - 1 - ly),
    (1, 1): (3, 0, lambda lx, ly, size: 0, lambda lx, ly, size: size - 1 - lx),
    (1, 2): (2, 2, lambda lx, ly, size: size - 1, lambda lx, ly, size: ly),
    (1, 3): (4, 2, lambda lx, ly, size: size - 1, lambda lx, ly, size: size - 1 - lx),

    (2, 0): (1, 0, lambda lx, ly, size: 0, lambda lx, ly, size: ly),
    (2, 1): (3, 3, lambda lx, ly, size: size - 1 - lx, lambda lx, ly, size: size - 1),
    (2, 2): (6, 3, lambda lx, ly, size: size - 1 - ly, lambda lx, ly, size: size - 1),
    (2, 3): (4, 3, lambda lx, ly, size: lx, lambda lx, ly, size: size - 1),

    (3, 0): (6, 0, lambda lx, ly, size: 0, lambda lx, ly, size: ly),
    (3, 1): (2, 3, lambda lx, ly, size: size - 1 - lx, lambda lx, ly, size: size - 1),
    (3, 2): (1, 3, lambda lx, ly, size: size - 1 - ly, lambda lx, ly, size: size - 1),
    (3, 3): (5, 1, lambda lx, ly, size: size - 1 - lx, lambda lx, ly, size: 0),

    (4, 0): (1, 1, lambda lx, ly, size: size - 1 - ly, lambda lx, ly, size: 0),
    (4, 1): (2, 1, lambda lx, ly, size: lx, lambda lx, ly, size: 0),
    (4, 2): (6, 2, lambda lx, ly, size: size - 1, lambda lx, ly, size: ly),
    (4, 3): (5, 3, lambda lx, ly, size: lx, lambda lx, ly, size: size - 1),

    (5, 0): (1, 2, lambda lx, ly, size: size - 1, lambda lx, ly, size: size - 1 - ly),
    (5, 1): (4, 1, lambda lx, ly, size: lx, lambda lx, ly, size: 0),
    (5, 2): (6, 1, lambda lx, ly, size: ly, lambda lx, ly, size: 0),
    (5, 3): (3, 1, lambda lx, ly, size: size - 1 - lx, lambda lx, ly, size: 0),

    (6, 0): (4, 0, lambda lx, ly, size: 0, lambda lx, ly, size: ly),
    (6, 1): (2, 0, lambda lx, ly, size: 0, lambda lx, ly, size: size - 1 - lx),
    (6, 2): (3, 2, lambda lx, ly, size: size - 1, lambda lx, ly, size: ly),
    (6, 3): (5, 0, lambda lx, ly, size: 0, lambda lx, ly, size: lx)
}

act_transitions = {
    (1, 0): (2, 3, lambda lx, ly, size: ly, lambda lx, ly, size: size - 1),
    (1, 1): (4, 1, lambda lx, ly, size: lx, lambda lx, ly, size: 0),
    (1, 2): (5, 1, lambda lx, ly, size: ly, lambda lx, ly, size: 0),
    (1, 3): (3, 3, lambda lx, ly, size: lx, lambda lx, ly, size: size - 1),

    (2, 0): (4, 2, lambda lx, ly, size: size - 1, lambda lx, ly, size: size - 1 - ly),
    (2, 1): (1, 2, lambda lx, ly, size: size - 1, lambda lx, ly, size: lx),
    (2, 2): (3, 2, lambda lx, ly, size: size - 1, lambda lx, ly, size: ly),
    (2, 3): (6, 3, lambda lx, ly, size: lx, lambda lx, ly, size: size - 1),

    (3, 0): (2, 0, lambda lx, ly, size: 0, lambda lx, ly, size: ly),
    (3, 1): (1, 1, lambda lx, ly, size: lx, lambda lx, ly, size: 0),
    (3, 2): (5, 0, lambda lx, ly, size: 0, lambda lx, ly, size: size - 1 - ly),
    (3, 3): (6, 0, lambda lx, ly, size: 0, lambda lx, ly, size: lx),

    (4, 0): (2, 2, lambda lx, ly, size: size - 1, lambda lx, ly, size: size - 1 - ly),
    (4, 1): (6, 2, lambda lx, ly, size: size - 1, lambda lx, ly, size: lx),
    (4, 2): (5, 2, lambda lx, ly, size: size - 1, lambda lx, ly, size: ly),
    (4, 3): (1, 3, lambda lx, ly, size: lx, lambda lx, ly, size: size - 1),

    (5, 0): (4, 0, lambda lx, ly, size: 0, lambda lx, ly, size: ly),
    (5, 1): (6, 1, lambda lx, ly, size: lx, lambda lx, ly, size: 0),
    (5, 2): (3, 0, lambda lx, ly, size: 0, lambda lx, ly, size: size - 1 - ly),
    (5, 3): (1, 0, lambda lx, ly, size: 0, lambda lx, ly, size: lx),

    (6, 0): (4, 3, lambda lx, ly, size: ly, lambda lx, ly, size: size - 1),
    (6, 1): (2, 1, lambda lx, ly, size: lx, lambda lx, ly, size: 0),
    (6, 2): (3, 1, lambda lx, ly, size: ly, lambda lx, ly, size: 0),
    (6, 3): (5, 3, lambda lx, ly, size: lx, lambda lx, ly, size: size - 1)
}


def parse_directions(line):
    directions = []
    number = ""
    for c in line:
        if c == 'R' or c == 'L':
            directions.append(int(number))
            directions.append(c)
            number = ""
        else:
            number += c

    if number != '':
        directions.append(int(number))

    return directions


def add_vertical_size(sizes, x, y, position):
    size = sizes.get(x)
    if size is None:
        size = [0, 0]
        sizes[x] = size

    size[position] = y


def parse_input(lines):
    grid = []
    directions = None
    sizes_h = {}
    sizes_v = {}

    for y, line in enumerate(lines):
        if line.strip() == '':
            directions = parse_directions(lines[y + 1].strip())
            break

        row = []
        grid.append(row)

        start_h = 0
        end_h = 0

        for x, c in enumerate(line):
            if c == '\n':
                continue

            row.append(c)

            if c == ' ' or c == '\n':
                if lines[y + 1] != '\n' and lines[y + 1][x] not in (' ', '\n'):
                    add_vertical_size(sizes_v, x, y + 1, 0)

                continue

            if x == 0 or line[x - 1] == ' ':
                start_h = x
            if x == len(line) - 1 or line[x + 1] in (' ', '\n'):
                end_h = x

            if y == 0 or (len(lines[y - 1]) - 1) <= x:
                add_vertical_size(sizes_v, x, y, 0)

            if lines[y + 1] == '\n' or (len(lines[y + 1]) - 1) <= x or lines[y + 1][x] == ' ':
                add_vertical_size(sizes_v, x, y, 1)

        sizes_h[y] = start_h, end_h

    return grid, directions, sizes_h, sizes_v


def elements_less_then(folds, value):
    count = 0
    for v in folds:
        if v <= value:
            count += 1
        else:
            break
    return count - 1


def generate_plane(size):
    return [[0 for _ in range(size)] for _ in range(size)]


def fold_cube(size, side_map, grid):
    folds_h = set()
    folds_v = set()

    max_x = 0

    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if x > max_x:
                max_x = x

            if c == ' ':
                continue

            if x % size == 0:
                folds_v.add(x)

            if y % size == 0:
                folds_h.add(y)

    folds_h = list(sorted(folds_h))
    folds_v = list(sorted(folds_v))

    top = generate_plane(size)
    bottom = generate_plane(size)
    north = generate_plane(size)
    south = generate_plane(size)
    east = generate_plane(size)
    west = generate_plane(size)

    side_num_to_plane = {
        1: top,
        6: bottom,
        4: north,
        3: south,
        5: east,
        2: west
    }

    start = None
    adjustment_map = {}

    for y, row in enumerate(grid):
        num_folds_h = elements_less_then(folds_h, y)

        for x, c in enumerate(row):
            if c == ' ':
                continue

            num_folds_v = elements_less_then(folds_v, x)

            side_num = side_map[(num_folds_h, num_folds_v)]
            if start is None:
                start = side_num

            side = side_num_to_plane[side_num]
            side[y % size][x % size] = c

            if y % size == 0 and x % size == 0:
                adjustment_map[side_num] = (folds_v[num_folds_v], folds_h[num_folds_h])

    return top, bottom, north, south, east, west, start, adjustment_map


def follow_path_on_cube(cube, size, directions, transitions):
    headings = ((1, 0), (0, 1), (-1, 0), (0, -1))
    top, bottom, north, south, east, west, side_num, adjustment_map = cube

    side_num_to_plane = {
        1: top,
        6: bottom,
        4: north,
        3: south,
        5: east,
        2: west
    }

    y = 0
    x = 0
    heading = 0
    side = side_num_to_plane[side_num]
    path_step = 0
    path = {}

    for c in directions:
        if c == 'R':
            adj_x, adj_y = adjustment_map[side_num]
            path[(x + adj_x, y + adj_y)] = path_step
            path_step += 1

            heading += 1
            if heading >= len(headings):
                heading = 0
            continue

        if c == 'L':
            adj_x, adj_y = adjustment_map[side_num]
            path[(x + adj_x, y + adj_y)] = path_step
            path_step += 1

            heading -= 1
            if heading < 0:
                heading = len(headings) - 1
            continue

        for step in range(c):
            adj_x, adj_y = adjustment_map[side_num]
            path[(x + adj_x, y + adj_y)] = path_step
            path_step += 1

            dx, dy = headings[heading]
            x_dx = x + dx
            y_dy = y + dy

            if y_dy < 0 or y_dy >= size or x_dx < 0 or x_dx >= size:
                next_side_num, next_heading, f_x, f_y = transitions[(side_num, heading)]
                next_x = f_x(x, y, size)
                next_y = f_y(x, y, size)

                next_side = side_num_to_plane[next_side_num]
                if next_side[next_y][next_x] == '#':
                    break
                else:
                    x = next_x
                    y = next_y
                    heading = next_heading
                    side_num = next_side_num
                    side = next_side
            elif side[y_dy][x_dx] == '#':
                break
            else:
                x = x_dx
                y = y_dy

    adj_x, adj_y = adjustment_map[side_num]

    return (x + adj_x + 1) * 4 + (y + adj_y + 1) * 1000 + heading


def find_and_fold(size, side_map, transitions, lines):
    grid, directions, sizes_h, sizes_v = parse_input(lines)
    cube = fold_cube(size, side_map, grid)

    return follow_path_on_cube(cube, size, directions, transitions)


def follow_path(data):
    grid, directions, sizes_h, sizes_v = data

    headings = ((1, 0), (0, 1), (-1, 0), (0, -1))

    y = 0
    x = sizes_h[y][0]
    heading = 0

    path = {(x, y): heading}

    for c in directions:
        if c == 'R':
            heading += 1
            if heading >= len(headings):
                heading = 0
            path[(x, y)] = heading
            continue

        if c == 'L':
            heading -= 1
            if heading < 0:
                heading = len(headings) - 1
            path[(x, y)] = heading
            continue

        dx, dy = headings[heading]
        for step in range(c):
            x_dx = x + dx
            y_dy = y + dy

            start_h, end_h = sizes_h[y]
            start_v, end_v = sizes_v[x]

            if x_dx < start_h:
                x_dx = end_h
            if x_dx > end_h:
                x_dx = start_h
            if y_dy < start_v:
                y_dy = end_v
            if y_dy > end_v:
                y_dy = start_v

            if grid[y_dy][x_dx] == '#':
                break

            x = x_dx
            y = y_dy
            path[(x, y)] = heading

    return (x + 1) * 4 + (y + 1) * 1000 + heading


def run():
    return find_and_fold(50, act_side_map, act_transitions, from_file("inputs/22_password"))


def main():
    test(6032, follow_path(parse_input(from_file("test_inputs/22_password"))))
    test(66292, follow_path(parse_input(from_file("inputs/22_password"))))

    test(5031, find_and_fold(4, test_side_map, test_transitions, from_file("test_inputs/22_password")))
    print(run())


if __name__ == '__main__':
    main()
