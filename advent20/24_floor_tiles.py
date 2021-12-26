from Util import test, from_file

odd_name_to_delta = {'e': (1, 0), 'se': (0, 1), 'sw': (-1, 1), 'w': (-1, 0), 'nw': (-1, -1), 'ne': (0, -1)}
even_name_to_delta = {'e': (1, 0), 'se': (1, 1), 'sw': (0, 1), 'w': (-1, 0), 'nw': (0, -1), 'ne': (1, -1)}


def read_lines(lines):
    tiles = {}

    for line in lines:
        tile_c = read_line(line)
        tile = tiles.get(tile_c, 0)
        tiles[tile_c] = 1 if tile == 0 else 0

    return tiles


def read_line(line):
    line = line.strip()
    i = 0
    x, y = 3, 3

    while i < len(line):
        c_1 = line[i]
        c_2 = line[i + 1] if i + 1 < len(line) else ''

        if c_1 == 's' or c_1 == 'n':
            direction = c_1 + c_2
            i += 2
        else:
            direction = c_1
            i += 1

        name_to_delta = even_name_to_delta if y % 2 == 0 else odd_name_to_delta
        dx, dy = name_to_delta[direction]
        x += dx
        y += dy

    return x, y


def update_world(floor):
    next_floor = {}
    next_floor_set = set()

    for x, y in floor:
        neighbours = 0
        name_to_delta = even_name_to_delta if y % 2 == 0 else odd_name_to_delta

        for dx, dy in name_to_delta.values():
            x_dx = x + dx
            y_dy = y + dy

            coord = (x_dx, y_dy)

            if coord in floor:
                neighbours += 1
                continue

            count = next_floor.get(coord, 0)
            next_floor[coord] = count + 1

        if 0 < neighbours <= 2:
            next_floor_set.add((x, y))

    for coord, count in next_floor.items():
        if count == 2:
            next_floor_set.add(coord)

    return next_floor_set


def run_floor(lines):
    tiles = set()
    for c, tile in read_lines(lines).items():
        if tile == 1:
            tiles.add(c)

    for i in range(100):
        tiles = update_world(tiles)

    return len(tiles)


def run():
    return run_floor(from_file('inputs/24_floor_tiles'))


if __name__ == '__main__':
    small_test_input = ['esew', 'nwwswee']
    test_input = "sesenwnenenewseeswwswswwnenewsewsw\n", "neeenesenwnwwswnenewnwwsewnenwseswesw\n", "seswneswswsenwwnwse\n", "nwnwneseeswswnenewneswwnewseswneseene\n", "swweswneswnenwsewnwneneseenw\n", "eesenwseswswnenwswnwnwsewwnwsene\n", "sewnenenenesenwsewnenwwwse\n", "wenwwweseeeweswwwnwwe\n", "wsweesenenewnwwnwsenewsenwwsesesenwne\n", "neeswseenwwswnwswswnw\n", "nenwswwsewswnenenewsenwsenwnesesenew\n", "enewnwewneswsewnwswenweswnenwsenwsw\n", "sweneswneswneneenwnewenewwneswswnese\n", "swwesenesewenwneswnwwneseswwne\n", "enesenwswwswneneswsenwnewswseenwsese\n", "wnwnesenesenenwwnenwsewesewsesesew\n", "nenewswnwewswnenesenwnesewesw\n", "eneswnwswnwsenenwnwnwwseeswneewsenese\n", "neswnwewnwnwseenwseesewsenwsweewe\n", "wseweeenwnesenwwwswnew\n",

    test(10, sum(read_lines(test_input).values()))
    test(230, sum(read_lines(from_file('inputs/24_floor_tiles')).values()))
    #
    test(2208, run_floor(test_input))
    print(run())
