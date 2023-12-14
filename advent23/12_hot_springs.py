from Util import test, from_file


def parse(lines, expand):
    formats = []
    for line in lines:
        springs, numbers = line.strip().split()

        if expand:
            springs = (("%s?" % springs) * 5)[:-1]
            numbers = (("%s," % numbers) * 5)[:-1]

        springs = list(springs)
        numbers = list(map(int, numbers.split(",")))

        formats.append((springs, numbers))

    return formats


def find_corrupted(springs):
    corruptions = []
    for i, c in enumerate(springs):
        if c == '?':
            corruptions.append(i)
    return corruptions


def reconstruct(springs, numbers):
    corruptions = find_corrupted(springs)

    options = [springs]

    for corruption in corruptions:
        next_options = []
        for option in options:
            operational = list(option)
            operational[corruption] = '.'

            damaged = list(option)
            damaged[corruption] = '#'

            if is_valid(operational, numbers):
                next_options.append(operational)

            if is_valid(damaged, numbers):
                next_options.append(damaged)

        options = next_options

    # print("Options: %d" % len(options))
    return len(options)


def is_valid_old(springs, numbers):
    groups = []
    group = 0

    for spring in springs:
        if spring == '#':
            group += 1
        if spring == '.':
            if group != 0:
                groups.append(group)
            group = 0
    if group != 0:
        groups.append(group)

    return groups == numbers


def is_valid(springs, numbers):
    group = 0
    group_index = list(numbers)

    for spring in springs:
        if spring == '?':
            return True
        if spring == '#':
            group += 1
        if spring == '.':
            if group != 0:
                if len(group_index) <= 0:
                    return False

                expected_group = group_index.pop(0)
                if group != expected_group:
                    return False
            group = 0
    if group != 0:
        if len(group_index) <= 0:
            return False

        expected_group = group_index.pop(0)
        if group != expected_group:
            return False

    return len(group_index) == 0


def is_valid_test(springs, numbers):
    old = is_valid_old(springs, numbers)
    new = is_valid(springs, numbers)

    if old != new:
        print("e: %s, a: %s, springs: %s" % (old, new, springs))

    return old and new


def validate_all(springs, numbers):
    count = 0
    for spring in springs:
        if is_valid(spring, numbers):
            count += 1
    return count


def reconstruct_all(formats):
    total = 0
    for springs, numbers in formats:
        reconstructed = reconstruct(springs, numbers)

        total += reconstructed

    return total


def part_1(lines):
    return reconstruct_all(parse(lines, False))


def part_2(lines):
    return reconstruct_all(parse(lines, True))


def main():
    test(21, part_1(from_file("test_inputs/12_hot_springs")))
    test(7251, part_1(from_file("inputs/12_hot_springs")))

    # test(525152, part_2(from_file("test_inputs/12_hot_springs")))
    # print(part_2(from_file("inputs/12_hot_springs")))


if __name__ == '__main__':
    main()
