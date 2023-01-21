from Util import test, test_is_not_incorrect, test_is_not_too_low, test_is_not_too_big


def generate(previous_value, factor):
    return (previous_value * factor) % 2147483647


def low_bits(value_a):
    return bin(value_a)[-16:]


def part_1(start_a, factor_a, start_b, factor_b):
    count = 0
    value_a = start_a
    value_b = start_b

    for step in range(40000000):
        value_a = generate(value_a, factor_a)
        value_b = generate(value_b, factor_b)

        bin_str_a = low_bits(value_a)
        bin_str_b = low_bits(value_b)

        if bin_str_a == bin_str_b:
            count += 1

    return count


def part_2(start_a, factor_a, start_b, factor_b):
    count = 0
    value_a = start_a
    value_b = start_b


    test_a = None
    test_b = None

    pairs_checked = 0

    while pairs_checked <= 5000001:
        if test_a is None:
            value_a = generate(value_a, factor_a)
        if test_b is None:
            value_b = generate(value_b, factor_b)

        if value_a % 4 == 0:
            test_a = value_a
        if value_b % 8 == 0:
            test_b = value_b

        if test_a is None or test_b is None:
            continue

        if low_bits(test_a) == low_bits(test_b):
            count += 1

        test_a = None
        test_b = None

        pairs_checked += 1

    return count


def main():
    test(588, part_1(65, 16807, 8921, 48271))
    test(567, part_1(512, 16807, 191, 48271))

    test(309, part_2(65, 16807, 8921, 48271))
    print(part_2(512, 16807, 191, 48271))


if __name__ == '__main__':
    main()
