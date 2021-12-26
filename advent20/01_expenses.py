from Util import test, from_file


def find_numbers(records, target):
    for record in records:
        other = target - record

        if other in records:
            return record, other


def find_numbers3(records, target):
    for first_record in records:
        for second_record in records:
            if first_record == second_record:
                continue

            other = target - second_record - first_record

            if other in records:
                return first_record, second_record, other


def fold(start, action, collection):
    for value in collection:
        start = action(start, value)
    return start


def find_and_multiply(records, target, f):
    numbers = f(records, target)

    return fold(1, lambda f, s: f * s, numbers)


def to_set(lines):
    records = set()

    for line in lines:
        records.add(int(line))

    return records


def run():
    return find_and_multiply(to_set(from_file("inputs/01_expenses")), 2020, find_numbers3)


if __name__ == '__main__':
    test(514579, find_and_multiply({1721, 979, 366, 299, 675, 1456}, 2020, find_numbers))
    test(926464, find_and_multiply(to_set(from_file("inputs/01_expenses")), 2020, find_numbers))

    test(241861950, find_and_multiply({1721, 979, 366, 299, 675, 1456}, 2020, find_numbers3))

    print(run())