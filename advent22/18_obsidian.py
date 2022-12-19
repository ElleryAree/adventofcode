from Util import test, from_file

empty_map = {}


class Cube:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

        self.__top = 1
        self.__bottom = 1
        self.__north = 1
        self.__south = 1
        self.__east = 1
        self.__west = 1

    def is_open_on_top(self):
        return self.__top > 0

    def is_open_on_bottom(self):
        return self.__bottom > 0

    def is_open_on_north(self):
        return self.__north > 0

    def is_open_on_south(self):
        return self.__south > 0

    def is_open_on_east(self):
        return self.__east > 0

    def is_open_on_west(self):
        return self.__west > 0

    def close_top(self):
        if self.__top == 1:
            self.__top = 0

    def close_bottom(self):
        if self.__bottom == 1:
            self.__bottom = 0

    def close_north(self):
        if self.__north == 1:
            self.__north = 0

    def close_south(self):
        if self.__south == 1:
            self.__south = 0

    def close_east(self):
        if self.__east == 1:
            self.__east = 0

    def close_west(self):
        if self.__west == 1:
            self.__west = 0

    def open_sides(self):
        return self.__top + self.__bottom + self.__north + self.__south + self.__east + self.__west

    def __str__(self):
        return "%d %d %d, open: %d" % (self.x, self.y, self.z, self.open_sides())


def parse_input(lines):
    min_x = 100000000
    max_x = -min_x

    min_y = 100000000
    max_y = -min_y

    min_z = 100000000
    max_z = -min_z

    cubes = []
    for line in lines:
        x, y, z = list(map(int, line.strip().split(",")))

        if x > max_x:
            max_x = x
        if x < min_x:
            min_x = x

        if y > max_y:
            max_y = y
        if y < min_y:
            min_y = y

        if z > max_z:
            max_z = z
        if z < min_z:
            min_z = z

        cubes.append(Cube(x, y, z))

    return cubes, min_x, max_x, min_y, max_y, min_z, max_z


def close_sides(cube, other_cube):
    if other_cube is None:
        return

    # top - bottom
    if cube.x == other_cube.x and cube.y == other_cube.y:
        if cube.z > other_cube.z:
            top = cube
            bottom = other_cube
        else:
            top = other_cube
            bottom = cube

        top.close_bottom()
        bottom.close_top()

    # west - east
    if cube.z == other_cube.z and cube.y == other_cube.y:
        if cube.x > other_cube.x:
            west = cube
            east = other_cube
        else:
            west = other_cube
            east = cube

        west.close_east()
        east.close_west()

    # north - south
    if cube.z == other_cube.z and cube.x == other_cube.x:
        if cube.y > other_cube.y:
            north = cube
            south = other_cube
        else:
            north = other_cube
            south = cube

        north.close_south()
        south.close_north()


def find_adjacent(cubes, cube):
    x, y, z = cube.x, cube.y, cube.z

    cube_down = cubes.get(z - 1, empty_map).get(y, empty_map).get(x)

    plane_on = cubes.get(z, empty_map)
    cube_on_left = plane_on.get(y - 1, empty_map).get(x)
    cube_on_right = plane_on.get(y + 1, empty_map).get(x)

    row_on = plane_on.get(y, empty_map)
    cube_on_on_left = row_on.get(x - 1)
    cube_on_on_right = row_on.get(x + 1)

    cube_up = cubes.get(z + 1, empty_map).get(y, empty_map).get(x)

    close_sides(cube, cube_down)
    close_sides(cube, cube_up)
    close_sides(cube, cube_on_left)
    close_sides(cube, cube_on_right)
    close_sides(cube, cube_on_on_left)
    close_sides(cube, cube_on_on_right)


def drop_into_water(_, cubes, min_x, max_x, min_y, max_y, min_z, max_z):
    run_min_x = min_x - 2
    run_max_x = max_x + 2
    run_min_y = min_y - 2
    run_max_y = max_y + 2
    run_min_z = min_z - 2
    run_max_z = max_z + 2
    
    filled = {}
    all_filled = []
    queue = [(run_min_x, run_min_y, run_min_z)]

    visited = set()

    while len(queue) > 0:
        c = queue.pop(0)

        if c in visited:
            continue
        visited.add(c)

        x, y, z = c
        cube = Cube(x, y, z)
        cube.is_air = True
        if x == run_min_x:
            cube.close_west()
        if x == run_max_x:
            cube.close_east()
        if y == run_min_y:
            cube.close_north()
        if y == run_max_y:
            cube.close_south()
        if z == run_min_z:
            cube.close_bottom()
        if z == run_max_z:
            cube.close_top()

        add_cube(filled, cube)
        all_filled.append(cube)


        for dx, dy, dz in ((-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)):
            x_dx = x + dx
            y_dy = y + dy
            z_dz = z + dz

            if x_dx < run_min_x or x_dx > run_max_x or y_dy < run_min_y or y_dy > run_max_y or z_dz < run_min_z or z_dz > run_max_z:
                continue

            if x_dx in cubes.get(z_dz, empty_map).get(y_dy, empty_map):
                continue

            queue.append((x_dx, y_dy, z_dz))

    filtered = list(filter(lambda c: (min_x - 1) <= c.x <= (max_x + 1) and (min_y - 1) <= c.y <= (max_y + 1) and (min_z - 1) <= c.z <= (max_z + 1), all_filled))
    return sum(map(lambda c: c.open_sides(), filtered))


def add_cube(cubes, cube):
    x, y, z = cube.x, cube.y, cube.z

    plane = cubes.get(z)
    if plane is None:
        plane = {}
        cubes[z] = plane

    row = plane.get(y)
    if row is None:
        row = {}
        plane[y] = row

    if x not in row:
        row[x] = cube
        find_adjacent(cubes, cube)


def calculate_sides(cubes, added, min_x, max_x, min_y, max_y, min_z, max_z):
    return sum(map(lambda c: c.open_sides(), cubes))


def find_sides(cubes, f):
    added_cubes = {}
    cubes, min_x, max_x, min_y, max_y, min_z, max_z = cubes

    for cube in cubes:
        add_cube(added_cubes, cube)

    return f(cubes, added_cubes, min_x, max_x, min_y, max_y, min_z, max_z)


def run():
    return find_sides(parse_input(from_file("inputs/18_obsidian")), drop_into_water)


def main():
    test(64, find_sides(parse_input(from_file("test_inputs/18_obsidian")), calculate_sides))
    test(4482, find_sides(parse_input(from_file("inputs/18_obsidian")), calculate_sides))

    test(58, find_sides(parse_input(from_file("test_inputs/18_obsidian")), drop_into_water))
    print(run())


if __name__ == '__main__':
    main()
