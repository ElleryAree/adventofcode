from Util import test, from_file


def part_1(line):
    return max(line) - min(line)

def part_2(line):
    for i in line:
        for j in line:
            if i == j:
                continue

            if i % j == 0:
                return int(i / j if i > j else j / i)

    return 0

def check_all(lines, f):
    return sum(map(lambda line: f(list(map(int, line.strip().split()))), lines))


def main():
    test(18, check_all(from_file("test_inputs/02_spreadsheet"), part_1))
    test(37923, check_all(from_file("inputs/02_spreadsheet"), part_1))

    test(9, check_all(from_file("test_inputs/02_spreadsheet_2"), part_2))
    print(check_all(from_file("inputs/02_spreadsheet"), part_2))


if __name__ == '__main__':
    main()
