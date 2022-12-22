from Util import test, from_file


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


def print_grid(grid, path):
    headings = {
        0: '>',
        1: 'v',
        2: '<',
        3: '^'
    }

    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            path_step = path.get((x, y))

            if path_step is not None:
                print(headings[path_step], end="")
            else:
                print(c, end='')
        print()
    print()


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

    # print_grid(grid, path)

    return (x + 1) * 4 + (y + 1) * 1000 + heading


def main():
    test(6032, follow_path(parse_input(from_file("test_inputs/22_password"))))
    print(follow_path(parse_input(from_file("inputs/22_password"))))


if __name__ == '__main__':
    main()
