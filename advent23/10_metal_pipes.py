from Util import from_file, test


def find_start(lines):
    for y, line in enumerate(lines):
        if "S" not in line:
            continue

        x = line.index('S')
        if x >= 0:
            return x, y


def is_valid_coord(x, y, lines):
    return 0 <= y < len(lines) and 0 <= x < len(lines[y])


def find_main_loop(lines):
    s_x, s_y = find_start(lines)

    visited = set()
    frontier = [(s_x, s_y, ())]

    while len(frontier) > 0:
        x, y, path = frontier.pop()

        if x == s_x and y == s_y:
            return path

        if (x, y) in visited:
            continue

        # up
        x_dx, y_dy = x, y - 1
        if is_valid_coord(x_dx, y_dy, lines):
            c = lines[y_dy][x_dx]

            if c in ('|'):
                pass

        # down

        # left

        # right

        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            x_dx = x + dx
            y_dy = y + dy

            if y_dy < 0 or y_dy >= len(lines) or x_dx < 0 or x_dx >= len(lines[y_dy]):
                continue


def find_pipes(x, y, lines):
    pipes = []

    # up
    x_dx, y_dy = x, y - 1
    if is_valid_coord(x_dx, y_dy, lines):
        c = lines[y_dy][x_dx]

        if c in ('|', '7', 'F'):
            pipes.append((0, -1))
    # down
    x_dx, y_dy = x, y + 1
    if is_valid_coord(x_dx, y_dy, lines):
        c = lines[y_dy][x_dx]

        if c in ('|', 'L', 'J'):
            pipes.append((0, 1))

    # left
    x_dx, y_dy = x - 1, y
    if is_valid_coord(x_dx, y_dy, lines):
        c = lines[y_dy][x_dx]

        if c in ('-', 'L', 'F'):
            pipes.append((-1, 0))

    # right
    x_dx, y_dy = x + 1, y
    if is_valid_coord(x_dx, y_dy, lines):
        c = lines[y_dy][x_dx]

        if c in ('-', '7', 'J'):
            pipes.append((1, 0))

    return pipes


def next_delta(c, dx, dy):
    if c == 'L':
        if dy > 0:
            return 1, 0
        else:
            return 0, -1

    if c == 'J':
        if dy > 0:
            return -1, 0
        else:
            return 0, -1

    if c == '7':
        if dy < 0:
            return -1, 0
        else:
            return 0, 1

    if c == 'F':
        if dy < 0:
            return 1, 0
        else:
            return 0, 1

    # if c == '|' or '-':
    return dx, dy


def follow_pipe(s_x, s_y, dx, dy, visited, distances, lines):
    prev_x = s_x
    prev_y = s_y
    distance = 0

    while True:
        coord = (prev_x, prev_y)
        if coord in visited:
            return dx, dy

        visited.add(coord)

        distances[coord] = distance
        distance += 1

        prev_x = prev_x + dx
        prev_y = prev_y + dy
        c = lines[prev_y][prev_x]

        dx, dy = next_delta(c, dx, dy)


def backtrack_pipe(s_x, s_y, dx, dy, distances, lines):
    prev_x = s_x
    prev_y = s_y
    distance = 0

    while True:
        prev_x = prev_x + dx
        prev_y = prev_y + dy
        c = lines[prev_y][prev_x]

        dx, dy = next_delta(c, dx, dy)

        distance += 1

        last_distance = distances[(prev_x, prev_y)]
        if last_distance == distance:
            return distance


def find_main_loop_simple(lines):
    s_x, s_y = find_start(lines)

    pipes = find_pipes(s_x, s_y, lines)
    visited = set()
    distances = {}

    most_distant_points = []

    for dx, dy in pipes:
        if (s_x + dx, s_y + dy) in visited:
            continue

        last_dx, last_dy = follow_pipe(s_x, s_y, dx, dy, visited, distances, lines)
        most_distant_point = backtrack_pipe(s_x, s_y, -last_dx, -last_dy, distances, lines)
        most_distant_points.append(most_distant_point)

    return max(most_distant_points)


def find_loop(lines):
    s_x, s_y = find_start(lines)

    pipes = find_pipes(s_x, s_y, lines)
    visited = set()

    for dx, dy in pipes:
        if (s_x + dx, s_y + dy) in visited:
            continue

        pipe_points = {}

        last_dx, last_dy = follow_pipe(s_x, s_y, dx, dy, visited, pipe_points, lines)
        if (-last_dx, -last_dy) in pipes:
            return set(pipe_points.keys())


def grey_c(c):
    return '\x1b[0;37;40m' + c + '\x1b[0m'


def green_c(c):
    return '\x1b[0;31;42m' + c + '\x1b[0m'


def white(c, inside):
    return ('\x1b[0;28;%dm' % (42 if inside else 40)) + c + '\x1b[0m'


def replace_with_box(c):
    if c == 'L':
        return u'\u2514'
    if c == 'F':
        return u'\u250C'
    if c == '7':
        return u'\u2510'
    if c == 'J':
        return u'\u2518'
    if c == '-':
        return u'\u2500'
    if c == '|':
        return u'\u2502'

    return c


def fill_inside_outside(lines, loop):
    grid = []
    count = 0

    for y, line in enumerate(lines):
        line = line.strip()
        grid_line = []
        grid.append(grid_line)
        horizontal = 0

        last_symbol_h = None

        for x, c in enumerate(line):
            if (x, y) in loop:
                if c == 'L' or c == 'F' or c == 'S':
                    if c == 'S' and last_symbol_h is None:
                        last_symbol_h = c
                    elif c != 'S':
                        last_symbol_h = c

                if c == '7' or c == 'J':
                    if (last_symbol_h == 'L' and c == '7') or (last_symbol_h == 'F' and c == 'J'):
                        horizontal += 1
                    last_symbol_h = None

                if c == '|':
                    horizontal += 1

                # grid_line.append(white(replace_with_box(c), horizontal % 2 != 0))
                grid_line.append(white(" ", horizontal % 2 != 0))

            else:
                if horizontal % 2 != 0:
                    grid_line.append(green_c('I'))
                    count += 1
                else:
                    grid_line.append(grey_c(' '))

    for line in grid:
        print("".join(line))

    return count


def test_fills(filename):
    lines = from_file(filename)

    loop = find_loop(lines)
    return fill_inside_outside(lines, loop)


def main():
    test(4, find_main_loop_simple(from_file("test_inputs/10_metal_pipes_simple")))
    test(8, find_main_loop_simple(from_file("test_inputs/10_metal_pipes_complex")))
    test(7107, find_main_loop_simple(from_file("inputs/10_metal_pipes")))

    test(1, test_fills("test_inputs/10_metal_pipes_simple"))
    test(4, test_fills("test_inputs/10_metal_pipes_test_fills_simple"))
    test(8, test_fills("test_inputs/10_metal_pipes_test_fills_complex"))
    test(10, test_fills("test_inputs/10_metal_pipes_test_fills_very_complex"))
    test(281, test_fills("inputs/10_metal_pipes"))


if __name__ == '__main__':
    main()
