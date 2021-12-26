from math import sqrt

import numpy as np

from Util import test, from_file

all_rotations = [[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
                 [[1, 0, 0], [0, 0, -1], [0, 1, 0]],
                 [[1, 0, 0], [0, -1, 0], [0, 0, -1]],
                 [[1, 0, 0], [0, 0, 1], [0, -1, 0]],
                 [[0, -1, 0], [1, 0, 0], [0, 0, 1]],
                 [[0, 0, 1], [1, 0, 0], [0, 1, 0]],
                 [[0, 1, 0], [1, 0, 0], [0, 0, -1]],
                 [[0, 0, -1], [1, 0, 0], [0, -1, 0]],
                 [[-1, 0, 0], [0, -1, 0], [0, 0, 1]],
                 [[-1, 0, 0], [0, 0, -1], [0, -1, 0]],
                 [[-1, 0, 0], [0, 1, 0], [0, 0, -1]],
                 [[-1, 0, 0], [0, 0, 1], [0, 1, 0]],
                 [[0, 1, 0], [-1, 0, 0], [0, 0, 1]],
                 [[0, 0, 1], [-1, 0, 0], [0, -1, 0]],
                 [[0, -1, 0], [-1, 0, 0], [0, 0, -1]],
                 [[0, 0, -1], [-1, 0, 0], [0, 1, 0]],
                 [[0, 0, -1], [0, 1, 0], [1, 0, 0]],
                 [[0, 1, 0], [0, 0, 1], [1, 0, 0]],
                 [[0, 0, 1], [0, -1, 0], [1, 0, 0]],
                 [[0, -1, 0], [0, 0, -1], [1, 0, 0]],
                 [[0, 0, -1], [0, -1, 0], [-1, 0, 0]],
                 [[0, -1, 0], [0, 0, 1], [-1, 0, 0]],
                 [[0, 0, 1], [0, 1, 0], [-1, 0, 0]],
                 [[0, 1, 0], [0, 0, -1], [-1, 0, 0]]]


all_rotations_matrices = list(map(np.array, all_rotations))


class Scanner:
    def __init__(self):
        self.__points = set()
        self.__distances = None

    def append(self, points):
        self.__points.add(points)

    def reset_distances(self):
        self.__distances = None

    def calculate_distances(self):
        if self.__distances is not None:
            return self.__distances

        distances = {}

        for x, y, z in self.__points:
            point = (x, y, z)
            for cx, cy, cz in self.__points:
                if x == cx and y == cy and z == cz:
                    continue

                point_2 = cx, cy, cz
                dist = sqrt((x - cx) ** 2 + (y - cy) ** 2 + (z - cz) ** 2)

                if dist not in distances:
                    distances[dist] = []

                if (point_2, point) not in distances[dist]:
                    distances[dist].append((point, point_2))

        self.__distances = distances
        return distances

    def get_points(self):
        return self.__points

    def rotate(self):
        scanners = []
        for rotation in all_rotations_matrices:
            scanner = Scanner()
            scanners.append(scanner)

            for point in self.__points:
                scanner.append(tuple(rotation.dot(np.array(point)).tolist()))

        return scanners

    def print_points(self):
        for x, y, z in self.__points:
            print("%2d, %2d, %2d" % (x, y, z))
        print()

    def __str__(self):
        return str(self.__points)


def parse_input(lines):
    scanner = None
    base_scanners = []

    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue

        if line[1] != '-':
            scanner.append(tuple(map(int, line.split(','))))
            continue

        scanner = Scanner()
        base_scanners.append(scanner)

    return base_scanners


def calculate_distances(scanner_positions):
    max_dist = 0

    for x, y, z in scanner_positions:
        for ox, oy, oz in scanner_positions:
            dist = abs(x - ox) + abs(y - oy) + abs(z - oz)
            if dist > max_dist:
                max_dist = dist

    return max_dist


def find_overlapping(lines):
    scanners = parse_input(lines)

    first_scanner = scanners[0]
    aligned_scanners = set()
    scanner_positions = [(0, 0, 0)]

    while len(aligned_scanners) < len(scanners) - 1:
        for i, scanner in enumerate(scanners[1:]):
            if i in aligned_scanners:
                continue

            scanner_position = align_scanners(first_scanner, scanner)
            if scanner_position:
                aligned_scanners.add(i)
                scanner_positions.append(scanner_position)

    return len(first_scanner.get_points()), calculate_distances(scanner_positions)


def align_scanners(first_scanner, second_scanner):
    for rotated_second in second_scanner.rotate():
        diff = compare_point_distances(first_scanner, rotated_second)
        if not diff:
            continue

        first_scanner.reset_distances()
        dx, dy, dz = diff
        for x, y, z in rotated_second.get_points():
            next_x = x + dx
            next_y = y + dy
            next_z = z + dz

            first_scanner.append((next_x, next_y, next_z))

        return diff


def calculate_diff(point1, point2):
    x1, y1, z1 = point1
    x2, y2, z2 = point2

    return x1 - x2, y1 - y2, z1 - z2


def compare_point_distances(first_points, second_points):
    first_distances = first_points.calculate_distances()
    second_distances = second_points.calculate_distances()

    hits = {}
    count = 0
    i = 0
    for dist, point_pairs in first_distances.items():
        if dist not in second_distances:
            continue

        second_point_pairs = second_distances[dist]
        i += 1
        for start, end in point_pairs:
            for s_start, s_end in second_point_pairs:
                diff_start = calculate_diff(start, s_start)
                diff_end = calculate_diff(end, s_end)

                diff_start_1 = calculate_diff(start, s_end)
                diff_end_1 = calculate_diff(end, s_start)

                if diff_start == diff_end:
                    if diff_start not in hits:
                        hits[diff_start] = set()

                    hits[diff_start].add(start)
                    hits[diff_start].add(end)
                    count += 1

                if diff_start_1 == diff_end_1:
                    if diff_start_1 not in hits:
                        hits[diff_start_1] = set()

                    hits[diff_start_1].add(start)
                    hits[diff_start_1].add(end)

    for diff, hits in hits.items():
        if len(hits) >= 12:
            return diff


def rotate():
    scanner = parse_input(['--- scanner 0 ---', '-1,-1,1', '-2,-2,2', '-3,-3,3', '-2,-3,1', '5,6,-4', '8,0,7'])

    test(24, len(scanner))


def run():
    return find_overlapping(from_file("inputs/19_beacons"))


def main():
    test_overlapping = find_overlapping(from_file("test_inputs/19_beacons"))
    test(79, test_overlapping[0])
    test(3621, test_overlapping[1])

    print(run())


if __name__ == '__main__':
    main()
