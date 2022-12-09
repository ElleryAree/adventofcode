from Util import from_file, test


class Rope:
    def __init__(self):
        self.__head_x = 0
        self.__head_y = 0
        self.__tail_x = 0
        self.__tail_y = 0

        self.__visited = {(0, 0)}

    def move(self, direction, steps):
        self.__move_head(self.__get_update(direction), steps)

    def print_grid(self, width, height):
        for y in range(height - 1, -1, -1):
            for x in range(width):
                if x == self.__head_x and y == self.__head_y:
                    print("H", end="")
                elif x == self.__tail_x and y == self.__tail_y:
                    print("T", end="")
                elif x == 0 and y == 0:
                    print("s", end="")
                else:
                    print(".", end="")
            print("")
        print("")

    def get_tail(self):
        return self.__tail_x, self.__tail_y

    def get_visited(self):
        return len(self.__visited)

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
            self.__head_x += dx
            self.__head_y += dy
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
        for dx, dy in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)):
            if self.__tail_x + dx == self.__head_x and self.__tail_y + dy == self.__head_y:
                return True
        return False

    def __move_tail(self):
        hor = self.__head_y - self.__tail_y
        ver = self.__head_x - self.__tail_x

        if self.__is_tail_adjacent():
            return

        self.__tail_x += self.__tail_delta(ver)
        self.__tail_y += self.__tail_delta(hor)

        self.__visited.add((self.__tail_x, self.__tail_y))


def update_rope_from_lines(lines):
    rope = Rope()
    # print("== Initial state ==")
    # rope.print_grid(6, 5)

    for line in lines:
        line = line.strip()

        # print("== %s == " % line)
        parts = line.split(" ")

        rope.move(parts[0], int(parts[1]))

    return rope.get_visited()


def main():
    test(13, update_rope_from_lines(from_file("test_inputs/09_tails")))
    test(5878, update_rope_from_lines(from_file("inputs/09_tails")))


if __name__ == '__main__':
    main()
