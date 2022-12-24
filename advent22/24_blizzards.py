from heapq import heappop, heappush

from Util import test, from_file


class BlizzardCache:
    def __init__(self):
        self.__filled = False
        self.__hashes = set()
        self.__step_to_blizzard = {}

    def add(self, step, blizzard, blizzard_hash):
        if not self.__filled and blizzard_hash in self.__hashes:
            self.__filled = True
            return
        self.__hashes.add(blizzard_hash)
        self.__step_to_blizzard[step] = (blizzard, blizzard_hash)

    def get(self, step):
        return self.__step_to_blizzard.get(step)


class State:
    def __init__(self, x, y, end_x, end_y, steps, blizzards, cache, blizzard_hash=None):
        self.x = x
        self.y = y
        self.steps = steps
        self.blizzard_hash = blizzard_hash

        self.__end_x = end_x
        self.__end_y = end_y

        self.__dist = abs(x - end_x) + abs(y - end_y)
        self.__blizzards = blizzards

        self.__cache = cache

    def __lt__(self, other):
        return (self.steps + self.__dist) < (other.steps + other.__dist)

    def __str__(self):
        return "%d %d, score (%d + %d)=%d" % (self.x, self.y, self.steps, self.__dist, self.steps + self.__dist)

    def get_blizzards(self):
        return self.__blizzards

    def next_step(self, next_x, next_y):
        next_blizzards = self.__blizzards
        return State(next_x, next_y, self.__end_x, self.__end_y, self.steps + 1, next_blizzards, self.__cache, self.blizzard_hash)

    def update_blizzards(self, width, height):
        cached = self.__cache.get(self.steps)
        if cached is not None:
            next_blizzards, next_hash = cached
            self.__blizzards = next_blizzards
            self.blizzard_hash = next_hash
            return

        next_blizzards = {}
        blizzard_hash = []

        for (x, y), cell in self.__blizzards.items():
            for blizzard_item in cell:
                next_x = x
                next_y = y

                if blizzard_item == '>':
                    next_x += 1
                    if next_x >= width - 1:
                        next_x = 1
                if blizzard_item == '<':
                    next_x -= 1
                    if next_x < 1:
                        next_x = width - 2

                if blizzard_item == 'v':
                    next_y += 1
                    if next_y >= height - 1:
                        next_y = 1

                if blizzard_item == '^':
                    next_y -= 1
                    if next_y < 1:
                        next_y = height - 2

                coord = (next_x, next_y)
                blizzard_hash.append(str((next_x, next_y, blizzard_item)))

                blizzard_cell = next_blizzards.get(coord)
                if blizzard_cell is None:
                    blizzard_cell = []
                    next_blizzards[coord] = blizzard_cell
                blizzard_cell.append(blizzard_item)

        self.__blizzards = next_blizzards
        self.blizzard_hash = ", ".join(sorted(blizzard_hash))
        self.__cache.add(self.steps, next_blizzards, self.blizzard_hash)

    def can_move(self, x, y):
        return (x, y) not in self.__blizzards

    def get_blizzard(self, x, y):
        return self.__blizzards.get((x, y))



def scan_grid(lines):
    blizzards = {}

    start_x = 0
    start_y = 0

    end_x = 0
    end_y = len(lines) - 1
    grid = []

    for y, line in enumerate(lines):
        line = line.strip()
        updated_line = ""
        for x, c in enumerate(line):
            if y == start_y and c == '.':
                start_x = x
            if y == end_y and c == '.':
                end_x = x

            if c in ('^', "v", '>', "<"):
                blizzards[(x, y)] = [c]
                updated_line += '.'
            else:
                updated_line += c
        grid.append(updated_line)

    return grid, blizzards, start_x, start_y, end_x, end_y


def find_path(start_step, blizzards, start_x, start_y, end_x, end_y, width, height, cache):
    frontier = [State(start_x, start_y, end_x, end_y, start_step, blizzards, cache, ())]
    visited = set()

    while len(frontier) > 0:
        state = heappop(frontier)

        coord = state.x, state.y, state.blizzard_hash
        if coord in visited:
            continue
        visited.add(coord)

        if state.x == end_x and state.y == end_y:
            return state

        state.update_blizzards(width, height)

        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            x_dx = state.x + dx
            y_dy = state.y + dy

            if (state.can_move(x_dx, y_dy) and 0 < x_dx < (width - 1) and 0 < y_dy < (height - 1)) or (x_dx == end_x and y_dy == end_y):
                heappush(frontier, state.next_step(x_dx, y_dy))

        if state.can_move(state.x, state.y):
            heappush(frontier, state.next_step(state.x, state.y))

    return -1



def find_answer(lines):
    lines, blizzards, start_x, start_y, end_x, end_y = scan_grid(lines)
    state = find_path(0, blizzards, start_x, start_y, end_x, end_y, len(lines[0]), len(lines), BlizzardCache())

    return state.steps


def there_and_back_again(lines):
    lines, blizzards, start_x, start_y, end_x, end_y = scan_grid(lines)
    cache = BlizzardCache()

    width = len(lines[0])
    height = len(lines)

    state = find_path(0, blizzards, start_x, start_y, end_x, end_y, width, height, cache)
    state_back = find_path(state.steps, state.get_blizzards(), end_x, end_y, start_x, start_y, width, height, cache)
    state_back_and_there = find_path(state_back.steps, state_back.get_blizzards(), start_x, start_y, end_x, end_y, width, height, cache)

    return state_back_and_there.steps


def run(lines):
    return there_and_back_again(lines)


def main():
    test_lines = from_file("test_inputs/24_blizzards")
    lines = from_file("inputs/24_blizzards")

    test(18, find_answer(test_lines))
    test(240, find_answer(lines))

    test(54, there_and_back_again(test_lines))
    print(run(lines))


if __name__ == '__main__':
    main()
