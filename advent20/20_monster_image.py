import re
from math import radians, cos, sin

from Util import from_file, test


class Tile:
    def __init__(self, direction='degree', degree=0, flip="non"):
        self.id = None
        self.direction = direction
        self.degree = degree
        self.flip = flip
        self.__data = []
        self.__top = -1
        self.__bottom = -1
        self.__left = -1
        self.__right = -1

    def add_line(self, line):
        self.__data.append(line)

    def set_id(self, tile_id):
        self.id = tile_id

    def complete(self):
        self.__top = self.__count_hash(self.__data[0])
        self.__bottom = self.__count_hash(self.__data[-1])
        self.__left = self.__count_hash(self.__build_side(0))
        self.__right = self.__count_hash(self.__build_side(-1))

    def name(self):
        return "%s-%6s-%s-%3d" % (self.id, self.direction, self.flip, self.degree)

    def top(self):
        return self.__top

    def bottom(self):
        return self.__bottom

    def left(self):
        return self.__left

    def right(self):
        return self.__right

    def data(self):
        return self.__data

    def __flip(self, tile):
        tile.flip = 'yes'
        for i in range(len(self.__data) - 1, -1, -1):
            tile.add_line(self.__data[i])

    def __rotate_left(self, tile, degree):
        data = []
        for _ in range(len(self.__data)):
            data.append([" " for _ in self.__data[0]])

        for j, line in enumerate(self.__data):
            for i, c in enumerate(line):
                ox = (len(line) - 1) / 2
                oy = (len(line) - 1) / 2
                ni, nj = self.__rotate(ox, oy, i, j, degree)
                data[nj][ni] = c

        for row in data:
            tile.add_line("".join(row))

    @staticmethod
    def __rotate(ox, oy, x, y, degree):
        theta = radians(degree)

        cs = cos(theta)
        sn = sin(theta)

        qx = round(ox + cs * (x - ox) - sn * (y - oy))
        qy = round(oy + sn * (x - ox) + cs * (y - oy))

        return qx, qy

    def rotate(self, direction, degree=0):
        tile = Tile(direction, degree, self.flip)
        tile.set_id(self.id)

        if direction == 'flip':
            self.__flip(tile)
        if direction == 'degree':
            self.__rotate_left(tile, degree)

        tile.complete()
        return tile

    @staticmethod
    def __count_hash(line):
        return int(line.replace(".", "0").replace("#", "1"), 2)

    def __build_side(self, i):
        side_line = []
        for line in self.__data:
            side_line.append(line[i])
        return "".join(side_line)

    def print_tile(self, with_name=True):
        if with_name:
            print("Tile %s" % self.name())

        for line in self.__data:
            print(line)
        print()

    def __str__(self):
        return self.id


def parse_lines(lines) -> map:
    tiles = {}
    tiles_count = 0
    tile = Tile()

    def add_tile(tile_to_add):
        tiles[tile_to_add.name()] = tile_to_add
        return tile_to_add

    for line in lines:
        line = line.strip()

        if line == '':
            tiles_count += 1

            tile.complete()
            add_tile(tile)

            for rotation in range(0, 360, 90):
                add_tile(tile.rotate("degree", rotation))

            tile = add_tile(tile.rotate("flip"))
            for rotation in range(0, 360, 90):
                add_tile(tile.rotate("degree", rotation))

            tile = Tile()
            continue

        if line[0] == 'T':
            tile.set_id(line[5:-1])
            continue

        tile.add_line(line)

    return tiles, tiles_count


def count(lines, answer_choser):
    tiles, tiles_count = parse_lines(lines)

    top_order = prepare_tiles(tiles, lambda tile: tile.top(), lambda tile: tile.bottom())
    columns = find_sequences(tiles, top_order)

    top_order = prepare_tiles(tiles, lambda tile: tile.left(), lambda tile: tile.right())
    rows = find_sequences(tiles, top_order)

    column_starts = generate_column_starts(columns)
    row_starts = generate_column_starts(rows)

    answer, picture = combine(columns, rows, tiles_count, column_starts, row_starts)

    return answer_choser(answer, picture)


def print_rotations(lines, tile_id):
    tiles, _ = parse_lines(lines)

    for tile in tiles.values():
        if tile.id == tile_id:
            tile.print_tile()


class Column:
    def __init__(self, first, second):
        self.tiles = [first, second]
        self.name = " ".join(map(lambda tile: tile.name(), self.tiles))

    def first(self):
        return self.tiles[0]

    def last(self):
        return self.tiles[-1]

    def set_last(self, column):
        self.tiles.extend(column.tiles[1:])
        self.name = " ".join(map(lambda tile: tile.name(), self.tiles))

    def drop_last(self):
        self.tiles = self.tiles[:-1]

    def __str__(self):
        return self.name


def prepare_tiles(tiles, top, bottom):
    top_order = []
    for tile in tiles.values():
        top_order.append((top(tile), "bottom", tile.name(), tile.id))
        top_order.append((bottom(tile), "up", tile.name(), tile.id))

    return list(sorted(top_order))


def find_sequences(tiles, top_order):
    matching = {}
    for tile_data in top_order:
        matching_tiles = matching.get(tile_data[0])
        if matching_tiles is None:
            matching_tiles = []
            matching[tile_data[0]] = matching_tiles

        matching_tiles.append(tile_data)

    firsts = {}
    all_pairs = set()

    for matching_tiles in matching.values():
        for first in matching_tiles:
            for second in matching_tiles:
                if first[1] != 'up' or second[1] != 'bottom' or first[3] == second[3]:
                    continue

                first_tile = tiles[first[2]]
                second_tile = tiles[second[2]]

                pair = Column(first_tile, second_tile)
                firsts[first_tile.name()] = pair
                all_pairs.add(pair)

    return arrange_pairs(all_pairs, firsts)


def arrange_pairs(all_pairs, firsts):
    final_columns = set()
    final_columns.update(all_pairs)

    while len(all_pairs) > 0:
        pair = all_pairs.pop()

        second_name = pair.last().name()
        next_pair = firsts.get(second_name)

        while next_pair is not None:
            pair.set_last(next_pair)
            if next_pair in final_columns:
                final_columns.remove(next_pair)

            second_name = pair.last().name()
            next_pair = firsts.get(second_name)

    return final_columns


def generate_column_starts(columns):
    return {column.tiles[0].name(): column for column in columns}


def combine(columns, rows, tiles_count, column_starts, row_starts):
    for column in columns:
        for row in rows:
            if column.first().name() != row.first().name():
                continue

            total = len(column.tiles) * len(row.tiles)
            if total != tiles_count:
                continue

            if validate_grid(column, row, column_starts, row_starts):
                picture = build_picture(column, row_starts)
                return get_answer(column, row, column_starts), picture


def get_answer(column, row, column_starts):
    top_left = column.tiles[0]
    top_right = row.tiles[-1]
    bottom_left = column.tiles[-1]

    right_column = column_starts[top_right.name()]
    bottom_right = right_column.tiles[-1]

    return int(top_left.id) * int(top_right.id) * int(bottom_left.id) * int(bottom_right.id)


def build_picture(column, row_starts):
    picture = []
    offset = 0

    for tile in column.tiles:
        row = row_starts[tile.name()].tiles

        first_row = row[0].data()[1:-1]
        for line in first_row:
            picture.append(line[1:-1])

        for row_tile in row[1:]:
            for i, line in enumerate(row_tile.data()[1:-1]):
                picture[offset + i] += line[1:-1]

        offset += len(first_row)

    tile = Tile()
    tile.set_id("picture")
    for line in picture:
        tile.add_line(line)

    return tile


def validate_grid(column, row, column_starts, row_starts):
    first_column = column
    for tile in row.tiles[1:]:
        next_column = column_starts.get(tile.name())
        if next_column is None:
            return False

        if len(column.tiles) != len(next_column.tiles):
            return False

        for i in range(len(column.tiles)):
            left_tile = column.tiles[i]
            right_tile = next_column.tiles[i]

            if left_tile.right() != right_tile.left():
                return False

        column = next_column

    for tile in first_column.tiles[1:]:
        next_row = row_starts.get(tile.name())
        if next_row is None:
            return False

        if len(row.tiles) != len(next_row.tiles):
            return False

        for i in range(len(row.tiles)):
            top_tile = row.tiles[i]
            bottom_tile = next_row.tiles[i]

            if top_tile.bottom() != bottom_tile.top():
                return False

        row = next_row

    return True


def find_sea_monster_in_lines(acc, head, body, legs, head_pattern, body_pattern, legs_pattern):
    body_match = body_pattern.match(body)
    if not body_match:
        return acc

    body_start = len(body_match.group(1))

    head_match = head_pattern.match(head, pos=body_start)
    legs_match = legs_pattern.match(legs, pos=body_start)

    if not head_match or not legs_match:
        body_start += 1
        return find_sea_monster_in_lines(acc, head[body_start:], body[body_start:], legs[body_start:], head_pattern, body_pattern, legs_pattern)

    head_start = len(head_match.group(1))
    legs_start = len(legs_match.group(1))

    if head_start != 0 or legs_start != 0:
        body_start += 1
        return find_sea_monster_in_lines(acc, head[body_start:], body[body_start:], legs[body_start:], head_pattern, body_pattern, legs_pattern)

    return find_sea_monster_in_lines(acc + 1, head[body_start + 20:], body[body_start + 20:], legs[body_start + 20:], head_pattern, body_pattern, legs_pattern)


def count_water_in_tile(lines):
    total = 0
    for line in lines:
        for c in line:
            if c == '#':
                total += 1

    return total


def find_sea_monster(tile):
    head_pattern = re.compile("(.*?)(.{18}#.).*")
    body_pattern = re.compile("(.*?)(#.{4}##.{4}##.{4}###).*")
    legs_pattern = re.compile("(.*?)(.#.{2}#.{2}#.{2}#.{2}#.{2}#.{3}).*")

    lines = tile.data()
    monsters = 0

    for i in range(len(lines) - 2):
        head = lines[i]
        body = lines[i + 1]
        legs = lines[i + 2]

        monsters += find_sea_monster_in_lines(0, head, body, legs, head_pattern, body_pattern, legs_pattern)

    if monsters > 0:
        return count_water_in_tile(lines) - (monsters * 15)
    else:
        return 0


def find_monster_in_all_rotations(tile):
    all_rotations = [tile]

    for rotation in range(0, 360, 90):
        all_rotations.append(tile.rotate("degree", rotation))

    tile = tile.rotate("flip")
    all_rotations.append(tile)
    for rotation in range(0, 360, 90):
        all_rotations.append(tile.rotate("degree", rotation))

    for rotation in all_rotations:
        answer = find_sea_monster(rotation)
        if answer > 0:
            return answer


def compare_pictures(actual, expected):
    if len(actual) != len(expected):
        return False

    for i in range(len(actual)):
        actual_line = actual[i]
        expected_line = expected[i]

        if actual_line != expected_line:
            return False

    return True


def run():
    return find_monster_in_all_rotations(count(from_file("inputs/20_monster_image"), lambda _, picture: picture))


if __name__ == '__main__':
    test_input = ["Tile 2311:\n", "..##.#..#.\n", "##..#.....\n", "#...##..#.\n", "####.#...#\n", "##.##.###.\n",
                  "##...#.###\n", ".#.#.#..##\n", "..#....#..\n", "###...#.#.\n", "..###..###\n", "\n", "Tile 1951:\n",
                  "#.##...##.\n", "#.####...#\n", ".....#..##\n", "#...######\n", ".##.#....#\n", ".###.#####\n",
                  "###.##.##.\n", ".###....#.\n", "..#.#..#.#\n", "#...##.#..\n", "\n", "Tile 1171:\n", "####...##.\n",
                  "#..##.#..#\n", "##.#..#.#.\n", ".###.####.\n", "..###.####\n", ".##....##.\n", ".#...####.\n",
                  "#.##.####.\n", "####..#...\n", ".....##...\n", "\n", "Tile 1427:\n", "###.##.#..\n", ".#..#.##..\n",
                  ".#.##.#..#\n", "#.#.#.##.#\n", "....#...##\n", "...##..##.\n", "...#.#####\n", ".#.####.#.\n",
                  "..#..###.#\n", "..##.#..#.\n", "\n", "Tile 1489:\n", "##.#.#....\n", "..##...#..\n", ".##..##...\n",
                  "..#...#...\n", "#####...#.\n", "#..#.#.#.#\n", "...#.#.#..\n", "##.#...##.\n", "..##.##.##\n",
                  "###.##.#..\n", "\n", "Tile 2473:\n", "#....####.\n", "#..#.##...\n", "#.##..#...\n", "######.#.#\n",
                  ".#...#.#.#\n", ".#########\n", ".###.#..#.\n", "########.#\n", "##...##.#.\n", "..###.#.#.\n", "\n",
                  "Tile 2971:\n", "..#.#....#\n", "#...###...\n", "#.#.###...\n", "##.##..#..\n", ".#####..##\n",
                  ".#..####.#\n", "#..#.#..#.\n", "..####.###\n", "..#.#.###.\n", "...#.#.#.#\n", "\n", "Tile 2729:\n",
                  "...#.#.#.#\n", "####.#....\n", "..#.#.....\n", "....#..#.#\n", ".##..##.#.\n", ".#.####...\n",
                  "####.#.#..\n", "##.####...\n", "##..#.##..\n", "#.##...##.\n", "\n", "Tile 3079:\n", "#.#.#####.\n",
                  ".#..######\n", "..#.......\n", "######....\n", "####.#..#.\n", ".#...#.##.\n", "#.#####.##\n",
                  "..#.###...\n", "..#.......\n", "..#.###...\n", "\n"]

    test(20899048083289, count(test_input, lambda answer, _: answer))
    test(111936085519519, count(from_file("inputs/20_monster_image"), lambda answer, _: answer))

    test(273, find_monster_in_all_rotations(count(test_input, lambda _, picture: picture)))
    test(1792, run())
