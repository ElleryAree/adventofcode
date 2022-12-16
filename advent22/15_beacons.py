import re

from Util import from_file, test

line_pattern = re.compile("Sensor at x=([-0-9]*), y=([-0-9]*): closest beacon is at x=([-0-9]*), y=([-0-9]*)")


def merge_pairs(pairs, new):
    new_start = new[0]
    new_end = new[-1]

    for pair in pairs:
        start = pair[0]
        end = pair[-1]

        if start <= new_start <= end + 1:
            if start <= new_end <= end:
                return pairs

            pairs.remove(pair)
            pair[-1] = new_end

            return merge_pairs(pairs, pair)

        if start - 1 <= new_end <= end:
            pairs.remove(pair)
            pair[0] = new_start

            return merge_pairs(pairs, pair)

        if new_start < start and new_end > end:
            pairs.remove(pair)
            return merge_pairs(pairs, new)

    pairs.append(new)

    pairs.sort(key=lambda pair: pair[0])
    return pairs


def parse_input(lines, target_y):
    beacons = []
    intersections = []
    
    for line in lines:
        match = line_pattern.match(line)
        if not match:
            continue

        sensor_x = int(match.group(1))
        sensor_y = int(match.group(2))
        beacon_x = int(match.group(3))
        beacon_y = int(match.group(4))

        beacons.append((sensor_x, sensor_y, beacon_x, beacon_y))

        range = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)
        range_to_target = abs(sensor_y - target_y)
        diff = range - range_to_target

        if diff > 0:
            intersection = [sensor_x - diff, sensor_x + diff]
            merge_pairs(intersections, intersection)

    count = 0
    for intersection in intersections:
        count += abs(intersection[-1]) + abs(intersection[0])

    return count


def parse_input_part2(lines, max_c):
    beacons = []

    for line in lines:
        match = line_pattern.match(line)
        if not match:
            continue

        sensor_x = int(match.group(1))
        sensor_y = int(match.group(2))
        beacon_x = int(match.group(3))
        beacon_y = int(match.group(4))
        dist = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)

        beacons.append((sensor_x, sensor_y, dist))

    for y in range(max_c):
        intersections = []

        for s_x, s_y, dist in beacons:
            range_to_target = abs(s_y - y)
            diff = dist - range_to_target

            if diff > 0:
                intersection = [max(0, s_x - diff), min(s_x + diff, max_c)]
                merge_pairs(intersections, intersection)

        if len(intersections) == 2:
            target_x = intersections[0][-1] + 1
            return target_x * 4000000 + y


def main():
    # test_merger()

    test(26, parse_input(from_file("test_inputs/15_beacons"), 10))
    test(4748135, parse_input(from_file("inputs/15_beacons"), 2000000))

    test(56000011, parse_input_part2(from_file("test_inputs/15_beacons"), 20))
    print(parse_input_part2(from_file("inputs/15_beacons"), 4000000))


def test_merger():
    #actual
    test([[0, 13], [15, 20]], merge_pairs([[0, 13], [15, 20]], [15, 17]))

    # insert
    test([[0, 3], [5, 6]], merge_pairs([[0, 3]], [5, 6]))
    test([[0, 3], [5, 6], [10, 13]], merge_pairs([[0, 3], [10, 13]], [5, 6]))
    test([[-5, -2], [0, 3]], merge_pairs([[0, 3]], [-5, -2]))
    test([[-10, -7], [-5, -2], [0, 3]], merge_pairs([[-10, -7], [0, 3]], [-5, -2]))
    # merge
    test([[0, 5], [7, 11]], merge_pairs([[0, 3], [7, 11]], [2, 5]))
    test([[0, 5]], merge_pairs([[0, 3]], [4, 5]))
    test([[-15, 3]], merge_pairs([[0, 3]], [-15, -1]))
    test([[0, 7]], merge_pairs([[0, 3], [5, 7]], [2, 6]))
    test([[0, 7]], merge_pairs([[0, 3], [6, 7]], [4, 5]))
    # devour
    test([[0, 7]], merge_pairs([[0, 7]], [4, 5]))
    test([[0, 7]], merge_pairs([[4, 5]], [0, 7]))
    test([[3, 7]], merge_pairs([[4, 5]], [3, 7]))
    test([[0, 6]], merge_pairs([[4, 5]], [0, 6]))


if __name__ == '__main__':
    main()
