from Util import test, from_file


def generate_letters():
    letters = set()
    for i in range(26):
        letters.add(chr(ord('A') + i))
    return letters


all_letters = generate_letters()


def find_start(lines):
    for x, c in enumerate(lines[0]):
        if c == '|':
            return x


def find_turn(x, y, x_dx, y_dy, lines):
    for a_dx, a_dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        x_a_dx = x_dx + a_dx
        y_a_dy = y_dy + a_dy

        if x == x_a_dx and y == y_a_dy:
            continue

        if y_a_dy < 0 or y_a_dy >= len(lines) or x_a_dx < 0 or x_a_dx >= len(lines[y_a_dy]):
            continue

        c = lines[y_a_dy][x_a_dx]

        if c in {'+', '|', '-'} or c in all_letters:
            return a_dx, a_dy


def follow(lines):
    lines = list(map(lambda line: list(line), lines))

    letters = []
    x = find_start(lines)
    y = 0

    dx = 0
    dy = 1

    steps = 0

    while True:

        x_dx = x + dx
        y_dy = y + dy

        if y_dy < 0 or y_dy >= len(lines) or x_dx < 0 or x_dx >= len(lines[y_dy]):
            return "".join(letters), steps

        steps += 1

        c = lines[y_dy][x_dx]
        if c == '+':
            dx, dy = find_turn(x, y, x_dx, y_dy, lines)
        if c in all_letters:
            letters.append(c)
        if c == ' ':
            return "".join(letters), steps

        x = x_dx
        y = y_dy


def main():
    test_seq, test_steps = follow(from_file("test_inputs/19_routing"))
    test("ABCDEF", test_seq)
    seq, steps = follow(from_file("inputs/19_routing"))
    test("HATBMQJYZ", seq)

    test(38, test_steps)
    print(seq, steps)


if __name__ == '__main__':
    main()

