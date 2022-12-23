from Util import from_file, test


def parse_input_to_list(mult, lines):
    numbers = []
    i_to_num = {}
    num_to_i = {}

    start = None

    for i, line in enumerate(lines):
        value = int(line.strip()) * mult

        if value == 0:
            start = i, value

        value = i, value

        i_to_num[len(numbers)] = value
        num_to_i[value] = len(numbers)
        numbers.append(value)

    return numbers, i_to_num, num_to_i, start


def scale_up_down(size, index):
    return (index % size + size) % size


def move_number(i_to_num, num_to_i, number, size):
    value = number[1]
    if value == 0:
        return

    index = num_to_i[number]

    if value > 0:
        next_index = (index + value) % (size - 1)
    else:
        next_index = size - 1 - ((size - 1 - index - value) % (size - 1))

    if next_index > index:
        for to_move in range(index, next_index):
            num_to_move = i_to_num[to_move + 1]

            i_to_num[to_move] = i_to_num[to_move + 1]
            num_to_i[num_to_move] -= 1

        num_to_i[number] = next_index
        i_to_num[next_index] = number
    else:
        for to_move in range(index - 1, next_index - 1, -1):
            num_to_move = i_to_num[to_move]

            i_to_num[to_move + 1] = i_to_num[to_move]
            num_to_i[num_to_move] += 1

        num_to_i[number] = next_index
        i_to_num[next_index] = number


def mix_numbers(times, data):
    numbers, i_to_num, num_to_i, start = data

    for i in range(times):
        for number in numbers:
            move_number(i_to_num, num_to_i, number, len(numbers))

    test_list_1 = []
    for other_i in sorted(i_to_num):
        test_list_1.append(i_to_num[other_i][1])

    return test_list_1, num_to_i, start


def find_at(indices, data):
    numbers, num_to_i, start = data
    total = 0

    i = num_to_i[start]
    for c in range(indices[-1] + 1):
        if c in indices:
            total += numbers[i]

        i += 1
        if i >= len(numbers):
            i = 0

    return total


def run():
    return find_at([1000, 2000, 3000], mix_numbers(10, parse_input_to_list(811589153, from_file("inputs/20_mixing"))))


def main():
    test(3, find_at([1000, 2000, 3000], mix_numbers(1, parse_input_to_list(1, from_file("test_inputs/20_mixing")))))
    test(17490, find_at([1000, 2000, 3000], mix_numbers(1, parse_input_to_list(1, from_file("inputs/20_mixing")))))

    test(1623178306, find_at([1000, 2000, 3000], mix_numbers(10, parse_input_to_list(811589153, from_file("test_inputs/20_mixing")))))
    print(run())


if __name__ == '__main__':
    main()
