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





def parse_cube(size, lines):
    folds_h = set()
    folds_v = set()

    sizes_h = {}
    sizes_v = {}

    for y, line in enumerate(lines):
        if line.strip() == '':
            break

        start_h = 0
        end_h = 0

        for x, c in enumerate(line):
            if c == '\n':
                continue

            if c == ' ':
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

            if x in sizes_v and (x - sizes_v[x][0] + 1) % size == 0:
                folds_h.add(x)

        sizes_h[y] = start_h, end_h
        if (y - start_h + 1) % size == 0:
            folds_v.add(y)

    for y, line in enumerate(lines[:-2]):
        for x, c in enumerate(line):
            if c == ' ':
                print(' ', end='')
            elif x in folds_h or y in folds_v:
                print('#', end='')
            else:
                print('.', end='')
        print()
    print()


def elements_less_then(list, value):
    count = 0
    for v in list:
        if v <= value:
            count += 1
        else:
            break
    return count - 1


def generate_plane(size):
    return [[0 for _ in range(size)] for _ in range(size)]


def custom_in(needle, heap):
    for val in heap:
        if val == needle:
            return True
    return False


def find_folds(size, side_map, data):
    grid, directions, sizes_h, sizes_v = data
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


    # top = generate_plane(size)
    # bottom = generate_plane(size)
    # north = generate_plane(size)
    # south = generate_plane(size)
    # east = generate_plane(size)
    # west = generate_plane(size)

    top = "1"
    bottom = "6"
    north = "4"
    south = "3"
    east = "5"
    west = "2"

    side_num_to_plane = {
        1: top,
        6: bottom,
        4: north,
        3: south,
        5: east,
        2: west
    }

    scaled_grid = []
    scaled_grid_n = []
    scaled_grid_n_2 = []
    for y, row in enumerate(grid):

        num_folds_h = elements_less_then(folds_h, y)

        scaled_row = []
        scaled_row_n = []
        scaled_row_n_2 = []

        for x, c in enumerate(row):
            if c == ' ':
                # print(' ' * 6, end=' ')
                val = ' ' * 6
                if val not in scaled_row:
                    scaled_row.append(val)
                    scaled_row_n.append(" ")
                    scaled_row_n_2.append(" ")
                continue


            num_folds_v = elements_less_then(folds_v, x)

            # print(num_folds_h + num_folds_v, end='')
            # print(plane, end='')
            # print((num_folds_h, num_folds_v), end=' ')
            val = str((num_folds_h, num_folds_v))
            plane = side_num_to_plane[side_map[(num_folds_h, num_folds_v)]]
            if val not in scaled_row:
                scaled_row.append(val)
                scaled_row_n.append(plane)
    #
    #
    #         # if y in folds_h:
    #         #     print('v', end="")
    #         # elif x in folds_v:
    #         #     print(">", end='')
    #         # elif x >= len(row) or row[x] == ' ':
    #         #     print(' ', end='')
    #         # else:
    #         #     print(".", end='')
        if scaled_row not in scaled_grid:
            scaled_grid.append(scaled_row)
            scaled_grid_n.append(scaled_row_n)
            scaled_grid_n_2.append(scaled_row_n_2)
        # print()
    # print()

    for scaled_row in scaled_grid:
        print(" ".join(scaled_row))
    print()

    for scaled_row in scaled_grid_n:
        print(" ".join(scaled_row))
    print()

    for scaled_row in scaled_grid_n_2:
        print(" ".join(scaled_row))
    print()


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
    test_side_map = {
        (2, 3): 1,
        (2, 2): 2,
        (1, 0): 3,
        (1, 2): 4,
        (0, 2): 5,
        (1, 1): 6
    }

    side_map = {
        (3, 0): 1,
        (2, 1): 2,
        (2, 0): 3,
        (0, 2): 4,
        (0, 1): 5,
        (1, 1): 6
    }

    # test(6032, follow_path(parse_input(from_file("test_inputs/22_password"))))
    # test(66292, follow_path(parse_input(from_file("inputs/22_password"))))

    find_folds(4, test_side_map, parse_input(from_file("test_inputs/22_password")))
    find_folds(50, side_map, parse_input(from_file("inputs/22_password")))

    # parse_cube(50, from_file("inputs/22_password"))


if __name__ == '__main__':
    main()
