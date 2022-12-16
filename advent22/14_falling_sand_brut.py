from Util import from_file, test


def parse_input(lines):
    grid = {}
    max_y = 0

    for line in lines:
        prev_point = None
        for point in line.strip().split(" -> "):
            x, y = point.split(",")
            x = int(x)
            y = int(y)

            if y > max_y:
                max_y = y

            if prev_point is None:
                prev_point = (x, y)
                continue

            prev_x, prev_y = prev_point
            prev_point = (x, y)

            if prev_x == x:
                start = min(prev_y, y)
                end = max(prev_y, y)

                for y in range(start, end + 1):
                    list = grid.get(y)
                    if list is None:
                        list = set()
                        grid[y] = list

                    list.add(x)

            if prev_y == y:
                start = min(prev_x, x)
                end = max(prev_x, x)

                for x in range(start, end + 1):
                    list = grid.get(y)
                    if list is None:
                        list = set()
                        grid[y] = list

                    list.add(x)

    return grid, max_y


default_set = set()


def fall_sand(grid, max_y, with_floor):
    point_x = 500
    point_y = 0

    while True:
        point_y += 1

        if not with_floor:
            if point_y > max_y:
                break
        else:
            if point_y == max_y + 2:
                current_row = grid.get(point_y - 1)
                if current_row is None:
                    current_row = set()
                    grid[point_y - 1] = current_row
                current_row.add(point_x)

                return point_x, point_y - 1

        row = grid.get(point_y, default_set)

        if point_x not in row:
            continue

        if point_x - 1 not in row:
            point_x -= 1
            continue
        elif point_x + 1 not in row:
            point_x += 1
            continue
        else:
            current_row = grid.get(point_y - 1)
            if current_row is None:
                current_row = set()
                grid[point_y - 1] = current_row
            current_row.add(point_x)

            return point_x, point_y - 1


def parse_and_fall(lines, with_floor=False):
    grid, max_y = parse_input(lines)
    count = 0

    while True:
        sand = fall_sand(grid, max_y, with_floor)
        if sand == (500, 0):
            count += 1
            break
        elif sand is not None:
            count += 1
        else:
            break

    return count


def run():
    return parse_and_fall(from_file("inputs/14_falling_sand"), True)


def main():
    test(24, parse_and_fall(from_file("test_inputs/14_falling_sand")))
    test(1078, parse_and_fall(from_file("inputs/14_falling_sand")))

    test(93, parse_and_fall(from_file("test_inputs/14_falling_sand"), True))
    print(run())


if __name__ == '__main__':
    main()
