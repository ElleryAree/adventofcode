from Util import from_file, test


class Rope:
    def __init__(self, name, track_visited, tail):
        self.name = name
        self.__x = 0
        self.__y = 0
        self.__tail = tail
        self.__visited = {(0, 0)} if track_visited else None

    def __str__(self):
        return "%s (%d, %d)" % (self.name, self.__x, self.__y)

    def move(self, direction, steps):
        self.__move_head(self.__get_update(direction), steps)

    def __get_name_for_coord(self, x, y):
        if x == self.__x and y == self.__y:
            return self.name

        if self.__tail is None:
            return "."

        return self.__tail.__get_name_for_coord(x, y)

    def print_grid(self, width, height):
        for y in range(height - 1, -1, -1):
            for x in range(width):
                c = self.__get_name_for_coord(x, y)
                print(c, end="")
            print("")
        print("")

    def get_visited(self):
        return len(self.__visited) if self.__visited is not None else 0

    def __update_visited(self):
        if self.__visited is not None:
            self.__visited.add((self.__x, self.__y))

    @staticmethod
    def __get_update(direction):
        if direction == 'R':
            return 1, 0
        if direction == 'L':
            return -1, 0
        if direction == 'U':
            return 0, 1
        if direction == 'D':
            return 0, -1
        return 0, 0

    def __move_head(self, update, steps):
        dx, dy = update

        for _ in range(steps):
            self.__x += dx
            self.__y += dy
            self.__move_tail()

            # self.print_grid(6, 5)

    @staticmethod
    def __tail_delta(value):
        if value > 0:
            return 1
        if value < 0:
            return -1
        return 0

    def __is_tail_adjacent(self):
        dist = max(abs(self.__x - self.__tail.__x), abs(self.__y - self.__tail.__y))
        return dist <= 1

    def __move_tail(self):
        if self.__tail is None or self.__is_tail_adjacent():
            return

        hor = self.__y - self.__tail.__y
        ver = self.__x - self.__tail.__x

        self.__tail.__x += self.__tail_delta(ver)
        self.__tail.__y += self.__tail_delta(hor)

        self.__tail.__update_visited()
        self.__tail.__move_tail()


def update_rope_with_one_tail_from_lines(lines):
    last = Rope('T', True, None)
    rope = Rope('H', False, last)
    return update_rope_from_lines(rope, last, lines)


def update_rope_with_nine_tail_from_lines(lines):
    last = Rope('10', True, None)
    rope = last

    for i in range(9, 0, -1):
        rope = Rope(str(i), False, rope)

    return update_rope_from_lines(rope, last, lines)


def update_rope_from_lines(rope, last, lines):
    # print("== Initial state ==")
    # rope.print_grid(6, 5)

    for line in lines:
        line = line.strip()

        # print("== %s == " % line)
        parts = line.split(" ")

        rope.move(parts[0], int(parts[1]))

    return last.get_visited()


def run():
    return update_rope_with_nine_tail_from_lines(from_file("inputs/09_tails"))


def main():
    test(13, update_rope_with_one_tail_from_lines(from_file("test_inputs/09_tails")))
    test(5878, update_rope_with_one_tail_from_lines(from_file("inputs/09_tails")))
    test(1, update_rope_with_nine_tail_from_lines(from_file("test_inputs/09_tails")))
    print(run())


if __name__ == '__main__':
    main()
