from Util import test, from_file


def map_x_to_cycle(lines):
    cycles = {}
    cycle = 1
    x = 1

    for line in lines:
        line = line.strip()

        if line == 'noop':
            add_cycle = 1
            add_x = 0
            cycles[cycle] = x
        else:
            add_cycle = 2
            add_x = int(line.split()[1])
            cycles[cycle] = x
            cycles[cycle + 1] = x

        cycle += add_cycle
        x += add_x

    return cycles


def calculate_signal(lines):
    cycles = map_x_to_cycle(lines)

    total = 0
    for cycle in (20, 60, 100, 140, 180, 220):
        total += cycle * cycles[cycle]

    return total


def draw(lines):
    cycles = map_x_to_cycle(lines)

    for i in range(240):
        pos = i % 40
        x = cycles.get(i + 1, 1)

        if i % 40 == 0 and i > 0:
            print()

        if pos == (x - 1) or pos == x or pos == (x + 1):
            print(u"\u2588", end="")
        else:
            print(" ", end="")

    print()
    print()


def main():
    test(13140, calculate_signal(from_file("test_inputs/10_signal_strs")))
    test(13720, calculate_signal(from_file("inputs/10_signal_strs")))

    draw(from_file("test_inputs/10_signal_strs"))
    draw(from_file("inputs/10_signal_strs"))


if __name__ == '__main__':
    main()
