from __future__ import annotations

from typing import Optional

from Util import test, from_file


class Cube:
    def __init__(self, cube_id, x1, x2, y1, y2, z1, z2, state):
        self.__id = cube_id
        self.__x1 = x1
        self.__x2 = x2
        self.__y1 = y1
        self.__y2 = y2
        self.__z1 = z1
        self.__z2 = z2
        self.__state = state


    def __overlaps(self, cube: Cube) -> bool:
        cond_1 = self.__x2 >= cube.__x1
        cond_2 = cube.__x2 >= self.__x1
        cond_3 = self.__z2 >= cube.__z1
        cond_4 = cube.__z2 >= self.__z1
        cond_5 = self.__y2 >= cube.__y1
        cond_6 = cube.__y2 >= self.__y1

        return cond_1 and cond_2 and cond_3 and cond_4 and cond_5 and cond_6

    def __eq__(self, other):
        return self.__state == other.__state and self.__x1 == other.__x1 and self.__x2 == other.__x2 \
               and self.__y1 == other.__y1 and self.__y2 == other.__y2 \
               and self.__z1 == other.__z1 and self.__z2 == other.__z2

    def get_coord(self):
        """
        :return: (state, ((x_start, x_end), (y_start, y_end), (z_start, z_end)))
        """
        return self.__state, ((self.__x1, self.__x2), (self.__y1, self.__y2), (self.__z1, self.__z2))

    def get_id(self):
        return self.__id

    def is_on(self):
        return self.__state == 'on'

    def get_state(self):
        return self.__state

    def invert(self):
        self.__state = 'off' if self.__state == 'on' else 'on'
        return self

    def overlap(self, cube: Cube) -> Optional[Cube]:
        if not self.__overlaps(cube):
            return None

        return self.__overlapping_cube(cube)

    @staticmethod
    def __overlapping_line(x1s, x1e, x2s, x2e):
        inter_s = x1s if x1s >= x2s else x2s
        inter_e = x1e if x1e <= x2e else x2e
        return inter_s, inter_e

    def __overlapping_cube(self, cube):
        (inter_x1, inter_x2) = self.__overlapping_line(self.__x1, self.__x2, cube.__x1, cube.__x2)
        (inter_y1, inter_y2) = self.__overlapping_line(self.__y1, self.__y2, cube.__y1, cube.__y2)
        (inter_z1, inter_z2) = self.__overlapping_line(self.__z1, self.__z2, cube.__z1, cube.__z2)

        if self.__state == 'on' and cube.__state == 'on':
            inter_state = 'off'
        elif self.__state == 'off' and cube.__state == 'off':
            inter_state = 'on'
        else:
            inter_state = cube.__state

        return Cube("%s - %s" % (self.__id, cube.__id), inter_x1, inter_x2, inter_y1, inter_y2, inter_z1, inter_z2, inter_state)

    def size(self):
        size = (self.__x2 - self.__x1 + 1) * (self.__y2 - self.__y1 + 1) * (self.__z2 - self.__z1 + 1)
        if self.__state == 'off':
            size *= -1

        return size

    def to_string(self):
        return "%s is %s: (%d, %d), (%d, %d), (%d, %d)" % (self.__id, self.__state, self.__x1, self.__x2, self.__y1, self.__y2, self.__z1, self.__z2)

    def __str__(self):
        return self.to_string()


def parse_input(lines):
    cubes = []

    for i, line in enumerate(lines):
        line = line.strip()
        state, coords = line.split(" ")
        xx, yy, zz = coords.split(",")
        x_start, x_end = xx.split("=")[1].split("..")
        y_start, y_end = yy.split("=")[1].split("..")
        z_start, z_end = zz.split("=")[1].split("..")

        x_start = int(x_start)
        x_end = int(x_end)
        y_start = int(y_start)
        y_end = int(y_end)
        z_start = int(z_start)
        z_end = int(z_end)

        cubes.append(Cube(i, x_start, x_end, y_start, y_end, z_start, z_end, state))

    return cubes


def find_intersections(cubes: list[Cube]):
    acc: list[Cube] = [cubes[0]]
    for cube in cubes[1:]:
        next_acc = []

        for prev_cube in acc:
            next_acc.append(prev_cube)
            overlap = prev_cube.overlap(cube)
            if overlap is not None:
                next_acc.append(overlap)

        if cube.is_on():
            next_acc.append(cube)

        acc = next_acc

    return acc


def calculate_size(cubes: list[Cube]):
    return sum(map(lambda cube: cube.size(), cubes))


def run_on(lines):
    cubes = parse_input(lines)
    intersections = find_intersections(cubes)
    return calculate_size(intersections)


def run():
    return run_on(from_file("inputs/22_reactor_reboot"))


def main():
    test(27, run_on(["on x=10..12,y=10..12,z=10..12"]))
    test(27, run_on(
        ["on x=10..12,y=10..12,z=10..12", "on x=10..12,y=10..12,z=10..12"]))
    test(27, run_on(
        ["on x=10..12,y=10..12,z=10..12",
         "on x=10..10,y=10..10,z=10..10"]))
    test(20, run_on(
        ["on x=10..12,y=10..12,z=10..12",
         "off x=9..11,y=9..11,z=9..11",
         "on x=10..10,y=10..10,z=10..10"]))
    test(46, run_on([
        "on x=10..12,y=10..12,z=10..12",
        "on x=11..13,y=11..13,z=11..13"]))
    test(46, run_on([
        "on x=10..12,y=10..12,z=10..12",
        "on x=11..13,y=11..13,z=11..13",
        "on x=10..10,y=10..10,z=10..10"]))
    test(38, run_on([
        "on x=10..12,y=10..12,z=10..12",
        "on x=11..13,y=11..13,z=11..13",
        "off x=9..11,y=9..11,z=9..11"]))
    test(39, run_on([
        "on x=10..12,y=10..12,z=10..12",
        "on x=11..13,y=11..13,z=11..13",
        "off x=9..11,y=9..11,z=9..11",
        "on x=10..10,y=10..10,z=10..10"]))
    test(40, run_on([
        "on x=10..12,y=10..12,z=10..12",
        "on x=11..13,y=11..13,z=11..13",
        "off x=9..11,y=9..11,z=9..11",
        "on x=10..10,y=10..10,z=10..10",
        "on x=11..13,y=11..13,z=11..13"]))

    test(590784, run_on(from_file("test_inputs/22_reactor_reboot")[:-2]))
    test(596598, run_on(from_file("inputs/22_reactor_reboot")[:20]))

    test(2758514936282235, run_on(from_file("test_inputs/22_reactor_reboot_part_2")))
    test(1199121349148621, run())


if __name__ == '__main__':
    main()
