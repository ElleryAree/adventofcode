from Util import test, from_file
from math import radians, cos, sin


class Waypoint:
    def __init__(self):
        self.__north = 1
        self.__east = 10

    def north(self):
        return self.__north

    def east(self):
        return self.__east

    def move(self, direction, value):
        if direction == 'N':
            self.__north += value
        elif direction == 'S':
            self.__north -= value
        elif direction == 'E':
            self.__east += value
        else:
            self.__east -= value

    def __rotate(self, degree):
        theta = radians(degree)

        cs = cos(theta)
        sn = sin(theta)

        cx = round(self.__east * cs - self.__north * sn)
        cy = round(self.__east * sn + self.__north * cs)

        self.__east = cx
        self.__north = cy

    def turn_right(self, value):
        self.__rotate(-value)

    def turn_left(self, value):
        self.__rotate(value)


class Ferry:
    def __init__(self):
        self.__waypoint = Waypoint()
        self.__north = 0
        self.__east = 0

    def run(self, instructions):
        for instruction in instructions:
            instruction = instruction.strip()
            command = instruction[0]
            value = int(instruction[1:])

            if command == 'F':
                self.__move(value)
            elif command in ('N', 'S', 'E', 'W'):
                self.__waypoint.move(command, value)
            elif command == 'R':
                self.__waypoint.turn_right(value)
            elif command == 'L':
                self.__waypoint.turn_left(value)

    def distance(self):
        return abs(self.__north) + abs(self.__east)

    def __move(self, value):
        self.__north += value * self.__waypoint.north()
        self.__east += value * self.__waypoint.east()


def run_lines(lines):
    ferry = Ferry()
    ferry.run(lines)

    return ferry.distance()


def run():
    return run_lines(from_file("inputs/12_ferry"))


if __name__ == '__main__':
    test_input = ["F10\n", "N3\n", "F7\n", "R90\n", "F11\n"]
    test(286, run_lines(test_input))

    print(run())
