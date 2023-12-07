from Util import from_file, test


class Range:
    def __init__(self, dest_start, source_start, range_len):
        self.dest_start = dest_start
        self.source_start = source_start
        self.range_len = range_len

    def contains(self, source_number):
        return self.source_start <= source_number <= self.source_end()

    def convert(self, source_number):
        return self.dest_start + (source_number - self.source_start)

    def source_end(self):
        return self.source_start + self.range_len - 1

    def dest_end(self):
        return self.dest_start + self.range_len - 1

    def __str__(self):
        return "%d -> %d to %d -> %d (%d)" % \
            (self.source_start, self.source_end(), self.dest_start, self.dest_end(), self.range_len)


def parse_seeds(lines):
    seeds_line = next_line(lines)
    lines.pop(0)

    return list(map(int, seeds_line.split(": ")[1].split()))


def parse_map(lines):
    next_line(lines)
    ranges = []

    while True:
        line = next_line(lines)
        if len(line) == 0:
            break

        dest_start, source_start, range_len = line.split()
        ranges.append(Range(int(dest_start), int(source_start), int(range_len)))

    return ranges


def next_line(lines):
    if len(lines) == 0:
        return ""
    return lines.pop(0).strip()


def parse(lines):
    seeds = parse_seeds(lines)

    maps = []
    while len(lines) > 0:
        maps.append(parse_map(lines))

    return seeds, maps


"""
i - input, s - source, d - dest, t - target
================
ii ss dd tt
23 -- -- 23
24 -- -- 24

25 25 17 17
26 26 18 18

27 -- -- 27

28 28 01 01
29 29 02 02
30 30 03 03

31 -- -- 31
"""
"""
================
if current range contains a_range
123456789
.i.A.i.A. = .i.iA.i. (2 range) done

ii ss dd tt
25 -- -- 25 
26 -- -- 26
27 27 11 11
28 28 12 12
29 29 13 13
30 30 14 14
-- 31 15 --
-- 32 16 --
-- -- -- --
"""

"""
================
if current range contains a_range (starts at the same time
123456789
.i.A.i.A. = .i.iA.i. (2 range) done

ii ss dd tt
-- -- -- --
27 27 11 11
28 28 12 12
29 29 13 13
30 30 14 14
-- 31 15 --
-- 32 16 --
-- -- -- --
"""

"""
================
if a_range intersects current range:

123456789
.A.i.A.i. = .i.Ai.i (2 ranges) continue

ii ss dd tt
-- -- -- --
-- 14 19 --
-- 15 20 --
16 16 21 21
17 17 22 22
18 18 23 23
19 - --  19
20 - --  20
-- -- -- --
"""
"""
================
if a_range intersects current range (and same end):

123456789
.A.i.A.i. = .i.Ai.i (2 ranges) continue

ii ss dd tt
-- -- -- --
-- 14 19 --
-- 15 20 --
16 16 21 21
17 17 22 22
18 18 23 23
-- -- -- --
"""
"""
================
if a_range contains current range:

123456789
.A.i.i.A. = ...i.i... done

ii ss dd tt
-- -- -- --
-- 57 09 --
-- 58 10 --
59 59 11 11
60 60 12 12
61 61 13 13
-- 62 14 --
-- 63 15 --
-- -- -- --
"""
"""
================
all togather

ii ss dd tt
-- 72 90 --
-- -- -- --
-- 14 45 --
15 15 46 46
16 16 47 47
17 -- -- 17
18 -- -- 18
19 19 01 01
20 20 02 02
-- 21 03 --
-- -- -- --
83 -- -- 83
-- -- -- --
-- 42 19 --
43 43 20 20
-- 44 21 --
-- 45 22 --
46 -- -- 46
47 47 88 88
48 -- -- 48
-- -- -- --
-- 1 32 --
-- 2 33 -- 

"""


def convert_ranges_to_pairs(ranges):
    pairs = []
    for a_range in ranges:
        pairs.append((a_range.dest_start, a_range.dest_end()))
    return pairs


def merge_range(start, end, conv_map):
    ranges = []

    current_range = Range(start, start, end - start + 1)

    for a_range in sorted(conv_map, key=lambda r: r.source_start):
        # if a_range is before current_range: .A..A.i..i. = .i..i.
        if a_range.source_end() < current_range.source_start:
            continue

        # if a_range intersects current range: .i.A.i.A. = .i.iA.i. (2 range) done
        if current_range.contains(a_range.source_start) and a_range.contains(current_range.source_end()):
            first_len = a_range.source_start - current_range.source_start
            if first_len > 0:
                ranges.append(Range(current_range.source_start, current_range.source_start, first_len))

            second_start = a_range.dest_start

            end_diff = a_range.source_end() - current_range.source_end()
            second_len = a_range.range_len - end_diff
            ranges.append(Range(second_start, second_start, second_len))

            current_range = None
            break

        # if a_range intersects current range: .A.i.A.i. = .i.Ai.i (2 ranges) continue
        if a_range.contains(current_range.source_start) and current_range.contains(a_range.source_end()):
            first_start = current_range.dest_start

            end_diff = current_range.source_end() - a_range.source_end()
            first_len = current_range.range_len - end_diff
            ranges.append(Range(a_range.convert(first_start), first_start, first_len))

            second_len = current_range.range_len - first_len
            current_range = Range(current_range.source_end() - second_len + 1,
                                  current_range.source_end() - second_len + 1, second_len)

        # if a_range contains current range: .A.i.i.A. = ...i.i... done
        if a_range.contains(current_range.source_start) and a_range.contains(current_range.source_end()):
            ranges.append(
                Range(a_range.convert(current_range.source_start), current_range.source_start, current_range.range_len))
            current_range = None
            break

        # if current range contains a_range: .i.A.A.i = iiA.Aii (3 ranges)
        if current_range.contains(a_range.source_start) and current_range.contains(a_range.source_end()):
            first_start = current_range.source_start
            first_len = a_range.source_start - current_range.source_start

            ranges.append(Range(first_start, first_start, first_len))
            ranges.append(Range(a_range.dest_start, a_range.dest_start, a_range.range_len))

            current_len = current_range.range_len - first_len - a_range.range_len
            current_start = current_range.source_start + first_len + a_range.range_len

            current_range = Range(current_start, current_start, current_len)

        # if a_range is after current range: .i..i.A..A. no ranges, done
        if a_range.source_start > current_range.source_end():
            break

    if current_range is not None and current_range.range_len > 0:
        ranges.append(current_range)

    return convert_ranges_to_pairs(ranges)


def merge_maps(points_from, map_to):
    all_ranges = []
    for (start, end) in points_from:
        ranges = merge_range(start, end, map_to)
        all_ranges.extend(ranges)
    all_ranges.sort()
    return all_ranges


def seeds_to_single_range(seeds):
    return list(map(lambda seed: [seed, seed], seeds))


def seeds_to_range(seeds):
    conv_map = []
    for i in range(0, len(seeds) - 1, 2):
        start = seeds[i]
        range_len = seeds[i + 1]

        conv_map.append((start, start + range_len - 1))

    return conv_map


def find_lowest_location(lines, converter):
    seeds, maps = parse(lines)
    ranges = converter(seeds)

    for conv_map in maps:
        ranges = merge_maps(ranges, conv_map)

    return min(map(lambda a_range: a_range[0], ranges))


def part_1(lines):
    return find_lowest_location(lines, seeds_to_single_range)


def part_2(lines):
    return find_lowest_location(lines, seeds_to_range)


def test_merge():
    current_contains_a_range_test()
    a_range_intersects_current()
    a_range_intersects_current_with_same_start()
    a_range_intersects_current_range()
    a_range_intersects_current_range_with_same_end()
    a_range_contains_current_range()
    all_together_test()


def current_contains_a_range_test():
    conv_map = [
        Range(1, 28, 3),
        Range(17, 25, 2)
    ]
    ranges = merge_range(23, 31, conv_map)
    print(".i.A.A.i = iiA.Aii (3 ranges)")
    for a_range in ranges:
        print(a_range)
    print()


def a_range_intersects_current():
    print(".i.A.i.A. = .i.iA.i. (2 range) done")
    conv_map = [Range(11, 27, 6)]

    ranges = merge_range(25, 30, conv_map)
    for a_range in ranges:
        print(a_range)
    print()


def a_range_intersects_current_with_same_start():
    print(".i.A.i.A. = .i.iA.i. (2 range) done")
    conv_map = [Range(11, 27, 6)]

    ranges = merge_range(27, 30, conv_map)
    for a_range in ranges:
        print(a_range)
    print()


def a_range_intersects_current_range():
    print(".A.i.A.i. = .i.Ai.i (2 ranges) continue")
    conv_map = [Range(19, 14, 5)]

    ranges = merge_range(16, 20, conv_map)
    for a_range in ranges:
        print(a_range)
    print()


def a_range_intersects_current_range_with_same_end():
    print(".A.i.A.i. = .i.Ai.i (2 ranges) continue")
    conv_map = [Range(19, 14, 5)]

    ranges = merge_range(16, 18, conv_map)
    for a_range in ranges:
        print(a_range)
    print()


def a_range_contains_current_range():
    print(".A.i.i.A. = ...i.i... done")
    conv_map = [Range(9, 57, 7)]

    ranges = merge_range(59, 61, conv_map)
    for a_range in ranges:
        print(a_range)
    print()


def all_together_test():
    print("All together test")
    conv_map = [
        Range(90, 72, 1),
        Range(45, 14, 3),
        Range(1, 19, 3),
        Range(19, 42, 4),
        Range(88, 47, 1),
        Range(32, 1, 6),
    ]

    ranges = merge_maps(((15, 20), (83, 83), (43, 43), (46, 48)), conv_map)
    for a_range in ranges:
        print(a_range)


def map_one_number(number, conversion_map):
    for a_range in conversion_map:
        if a_range.contains(number):
            return a_range.convert(number)

    return number


def brut_force_ranges(lines):
    seeds, maps = parse(lines)

    ranges = seeds_to_range(seeds)

    conversions = [["  0"]]
    all_seeds = []
    all_ranges = []

    colors = ['\033[95m',
              '\033[94m',
              '\033[96m',
              '\033[92m',
              '\033[93m',
              '\033[91m',
              '\033[1m',
              '\033[4m']

    color_id = -1
    last_number = -1
    for (start, end) in sorted(ranges):
        for i in range(start, end + 1):
            if i != last_number + 1:
                color_id += 1
                if color_id >= len(colors):
                    color_id = 0
            last_number = i

            conversions.append(["%s%3d\033[0m" % (colors[color_id], i)])
            all_seeds.append(i)

    for c, conv_map in enumerate(maps):
        conversions[0].append("%3d" % (c + 1))

        next_seeds = []
        last_number = -1
        color_id = -1
        for i, seed in enumerate(all_seeds):
            conv = map_one_number(seed, conv_map)

            if conv != last_number + 1:
                color_id += 1
                if color_id >= len(colors):
                    color_id = 0

            last_number = conv
            conversions[i + 1].append("%s%3d\033[0m" % (colors[color_id], conv))
            next_seeds.append(conv)

        all_seeds = next_seeds
        ranges = merge_maps(ranges, conv_map)
        all_ranges.append(list(ranges))

    for seeds in conversions:
        print(" ".join(seeds))

    for i, convs in enumerate(all_ranges):
        print("%d: %s" % (i + 1, " ".join(map(str, convs))))


def run():
    print(part_2(from_file("inputs/05_seed_to_location_map")))


def main():
    test_merge()
    brut_force_ranges(from_file("test_inputs/05_seed_to_location_map"))

    test(35, part_1(from_file("test_inputs/05_seed_to_location_map")))
    test(51580674, part_1(from_file("inputs/05_seed_to_location_map")))

    test(46, part_2(from_file("test_inputs/05_seed_to_location_map")))
    run()


if __name__ == '__main__':
    main()
