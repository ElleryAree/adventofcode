from Util import from_file, test


def compose_grid(lines):
    return [map(lambda l: int(l), line.strip()) for line in lines]


def find_trees(grid):
    count = 0
    for y, row in enumerate(grid):
        for x, tree in enumerate(row):
            if x == 0 or x == len(row) - 1 or y == 0 or y == len(grid) - 1:
                count += 1
                continue

            if check_tree(grid, tree, x, y):
                count += 1
    return count


def count_all_visible_trees(grid):
    max_tree = -1
    for y, row in enumerate(grid):
        for x, tree in enumerate(row):
            if x == 0 or x == len(row) - 1 or y == 0 or y == len(grid) - 1:
                continue

            count = count_visible_trees(grid, tree, x, y)
            if count > max_tree:
                max_tree = count

    return max_tree


def check_one(grid, tree, x, y, update):
    dx, dy = update
    x_dx = x + dx
    y_dy = y + dy

    while 0 <= y_dy < len(grid) and 0 <= x_dx < len(grid[y_dy]):
        if grid[y_dy][x_dx] >= tree:
            return False

        x_dx += dx
        y_dy += dy

    return True


def check_tree(grid, tree, x, y):
    for update in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        if check_one(grid, tree, x, y, update):
            return True

    return False


def count_visible_trees_in_one_direction(grid, tree, x, y, update):
    dx, dy = update
    x_dx = x + dx
    y_dy = y + dy
    count = 0
    while 0 <= y_dy < len(grid) and 0 <= x_dx < len(grid[y_dy]):
        count += 1
        if grid[y_dy][x_dx] >= tree:
            break

        x_dx += dx
        y_dy += dy

    return count


def count_visible_trees(grid, tree, x, y):
    total = 1
    for update in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        total *= count_visible_trees_in_one_direction(grid, tree, x, y, update)

    return total


def run():
    return count_all_visible_trees(compose_grid(from_file("inputs/08_tree_house")))


def main():
    test(21, find_trees(compose_grid(from_file("test_inputs/08_tree_house"))))
    test(1794, find_trees(compose_grid(from_file("inputs/08_tree_house"))))

    test(8, count_all_visible_trees(compose_grid(from_file("test_inputs/08_tree_house"))))
    print(run())


if __name__ == '__main__':
    main()
