from Util import test, from_file


def calculate_calories(lines, f):
    elfs = []

    current_elf = 0

    for line in lines:
        line = line.strip()
        if line == "":
            elfs.append(current_elf)
            current_elf = 0
            continue

        current_elf += int(line)

    return f(elfs)


def find_biggest(elfs):
    return max(elfs)


def find_biggest_three(elfs):
    sorted_elfs = list(sorted(elfs))
    return sorted_elfs[-1] + sorted_elfs[-2] + sorted_elfs[-3]


def run():
    return calculate_calories(from_file("inputs/01_calories"), find_biggest_three)


def main():
    test(24000, calculate_calories(from_file("test_inputs/01_calories"), find_biggest))
    test(72240, calculate_calories(from_file("inputs/01_calories"), find_biggest))

    test(45000, calculate_calories(from_file("test_inputs/01_calories"), find_biggest_three))
    print(run())


if __name__ == '__main__':
    main()
