from Util import test, from_file


def parse_input(lines):
    points = []
    folds = []

    reading_points = True

    for line in lines:
        line = line.strip()

        if len(line) == 0:
            reading_points = False
            continue

        if reading_points:
            x, y = line.split(",")
            x = int(x)
            y = int(y)

            points.append((x, y))
        else:
            text, coord = line.split("=")
            folds.append((text[-1], int(coord)))

    return points, folds


def print_fold(points, verbose):
    width = 0
    height = 0
    points_map = {}

    for x, y in points:
        if x > width:
            width = x
        if y > height:
            height = y

        if y not in points_map:
            points_map[y] = {}

        if x not in points_map[y]:
            points_map[y][x] = '#'

    count = 0

    for _, row in points_map.items():
        count += len(row)

    if verbose:
        empty = {}
        for y in range(height + 1):
            for x in range(width + 1):
                print(points_map.get(y, empty).get(x, " "), end="")
            print()
        print()

    return count


def do_fold_at_once(points, folds):
    for i in range(len(points)):
        x, y = points[i]

        for axis, coord in folds:
            if axis == 'x':
                if x > coord:
                    x = coord - (x - coord)
            else:
                if y > coord:
                    y = coord - (y - coord)

        points[i] = x, y


def run_one(lines):
    points, folds = parse_input(lines)
    do_fold_at_once(points, folds[:1])

    return print_fold(points, False)


def run_all_at_once(lines):
    points, folds = parse_input(lines)
    do_fold_at_once(points, folds)

    return print_fold(points, False)


def run():
    run_all_at_once(from_file("inputs/13_folds"))


def main():
    test(17, run_one(from_file("test_inputs/13_folds")))
    print(run_one(from_file("inputs/13_folds")))

    run_all_at_once(from_file("test_inputs/13_folds"))
    run()


if __name__ == '__main__':
    main()
