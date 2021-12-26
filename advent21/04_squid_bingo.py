from Util import test, from_file


class Grid:
    def __init__(self):
        self.__numbers = {}
        self.__columns = [0 for _ in range(5)]
        self.__rows = [0 for _ in range(5)]

    def add__grid_number(self, number, x, y):
        self.__numbers[number] = x, y

    def add_number(self, number):
        coord = self.__numbers.get(number)
        if coord is None:
            return

        x, y = coord
        self.__columns[x] += 1
        self.__rows[y] += 1
        self.__numbers[number] = None

        if self.__columns[x] == 5 or self.__rows[y] == 5:
            return self.__calculate_score(number)
        else:
            return None

    def __calculate_score(self, called_number):
        count = 0
        for number, coord in self.__numbers.items():
            if coord is not None:
                count += number

        return count * called_number


def parse_input(lines):
    numbers = map(int, lines[0].strip().split(","))

    grid = Grid()
    y = 0
    grids = [grid]

    for line in lines[2:]:
        line = line.strip()
        if len(line) == 0:
            grid = Grid()
            y = 0
            grids.append(grid)
            continue

        for x, number in enumerate(filter(lambda n: len(n) > 0, line.split(" "))):
            grid.add__grid_number(int(number), x, y)
        y += 1

    return numbers, grids


def win(numbers, grids):
    for number in numbers:
        for grid in grids:
            score = grid.add_number(number)

            if score is not None:
                return score


def loose(numbers, grids):
    won = 0
    for number in numbers:
        for i in range(len(grids)):
            grid = grids[i]
            if grid is None:
                continue

            score = grid.add_number(number)

            if score is not None:
                won += 1
                grids[i] = None

                if won == len(grids):
                    return score


def do_run(game, lines):
    numbers, grids = parse_input(lines)
    return game(numbers, grids)


def run():
    return do_run(loose, from_file("inputs/04_squid_bingo"))


def main():
    test(4512, do_run(win, from_file("test_inputs/04_squid_bingo")))
    test(63424, do_run(win, from_file("inputs/04_squid_bingo")))
    test(1924, do_run(loose, from_file("test_inputs/04_squid_bingo")))
    print(run())


if __name__ == '__main__':
    main()
