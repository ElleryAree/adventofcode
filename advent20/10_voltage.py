from Util import test, from_file


def read_voltages(lines):
    voltages = sorted(list(map(lambda line: int(line.strip()), lines)))

    voltages.insert(0, 0)
    voltages.append(voltages[-1] + 3)

    return voltages


def find_diffs(voltages):
    count_1 = 0
    count_3 = 0

    for i in range(len(voltages) - 1):
        voltage = voltages[i]
        next_voltage = voltages[i + 1]
        diff = next_voltage - voltage

        if diff == 1:
            count_1 += 1
        if diff == 3:
            count_3 += 1

    return count_1, count_3


def run_one(lines):
    return find_diffs(read_voltages(lines))


def run_res(lines):
    one, three = run(lines)
    return one * three


def find_options(i, voltages):
    voltage = voltages[i]
    options = []
    for j in range(i - 1, -1, -1):
        prev_voltage = voltages[j]
        diff = voltage - prev_voltage

        if diff > 3:
            break

        options.append(j)

    return options


def count_permutations(voltages):
    counts = {len(voltages) - 1: 1}

    for i in range(len(voltages) - 1, -1, -1):
        for option in find_options(i, voltages):
            option_count = counts.get(option, 0)
            counts[option] = option_count + counts[i]

    return counts[0]


def run_count(lines):
    return count_permutations(read_voltages(lines))


def run():
    run_count(from_file("inputs/10_voltage"))


if __name__ == '__main__':
    test_input = ["16\n", "10\n", "15\n", "5\n", "1\n", "11\n", "7\n", "19\n", "6\n", "12\n", "4\n"]
    test_input_2 = ["28\n", "33\n", "18\n", "42\n", "31\n", "14\n", "46\n", "20\n", "48\n", "47\n", "24\n", "23\n", "49\n", "45\n", "19\n", "38\n", "39\n", "11\n", "1\n", "32\n", "25\n", "35\n", "8\n", "17\n", "7\n", "9\n", "4\n", "2\n", "34\n", "10\n", "3\n"]

    test((7, 5), run_one(test_input))
    test((22, 10), run_one(test_input_2))

    # test(1700, run_res(from_file("inputs/10_voltage")))

    test(8, run_count(test_input))
    test(19208, run_count(test_input_2))

    print(run())
