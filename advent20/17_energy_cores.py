from Util import test


def generate_deltas():
    deltas = []
    for w in range(-1, 2):
        for z in range(-1, 2):
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if w == 0 and z == 0 and i == 0 and j == 0:
                        continue

                    deltas.append((w, z, i, j))

    return tuple(deltas)


def parse_input(lines):
    world = set()

    for j, line in enumerate(lines):
        line = line.strip()

        for i, c in enumerate(line):
            if c == '#':
                world.add((0, 0, i, j))

    return world


def update_world(world, deltas):
    next_world = {}
    next_world_set = set()

    for w, z, i, j in world:
        neighbours = 0
        for dw, dz, di, dj in deltas:
            w_dw = w + dw
            z_dz = z + dz
            i_di = i + di
            j_dj = j + dj

            coord = (w_dw, z_dz, i_di, j_dj)

            if coord in world:
                neighbours += 1
                continue

            count = next_world.get(coord, 0)
            next_world[coord] = count + 1

        if neighbours == 2 or neighbours == 3:
            next_world_set.add((w, z, i, j))

    for coord, count in next_world.items():
        if count == 3:
            next_world_set.add(coord)

    return next_world_set


def print_world(world, turn):
    layers = {}

    for z, x, y in world:
        if z not in layers:
            layers[z] = []

        layers[z].append((x, y))

    min_max_layers = {}
    for z, grid in layers.items():
        min_x = 100000
        max_x = -10000

        min_y = 100000
        max_y = -10000

        for x, y in grid:
            if x > max_x:
                max_x = x
            if x < min_x:
                min_x = x

            if y > max_y:
                max_y = y
            if y < min_y:
                min_y = y

        min_max_layers[z] = (min_x, max_x, min_y, max_y)

    print("after %s cycles" % turn)
    for z in sorted(min_max_layers):
        min_x, max_x, min_y, max_y = min_max_layers[z]

        print("z=%d" % z)
        for y in range(min_y, max_y + 1):
            row = []
            for x in range(min_x, max_x + 1):
                row.append("#" if (z, x, y) in world else ".")

            print("".join(row))
        print()
    print()


def run_lines(lines):
    deltas = generate_deltas()
    world = parse_input(lines)
    # print_world(world, "start")

    for i in range(6):
        world = update_world(world, deltas)
        # print_world(world, str(i))

    return len(world)


def run():
    return run_lines(actual_input)


actual_input = ["##..#.#.", "###.#.##", "..###..#", ".#....##", ".#..####", "#####...", "#######.", "#.##.#.#"]

if __name__ == '__main__':
    test_input = [".#.", "..#", "###"]

    test(848, run_lines(test_input))

    print(run())

