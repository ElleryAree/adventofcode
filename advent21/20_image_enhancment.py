from Util import from_file, test


def parse_input(lines):
    return lines[0], list(map(lambda line: line.strip(), lines[2:]))


def pixel_at(x, y, lines, step):
    if x < 0 or x >= len(lines[0]) or y < 0 or y >= len(lines):
        return "0" if step % 2 == 0 else '1'
    return "1" if lines[y][x] == '#' else '0'


def enhance(step, lines, algo):
    pattern_mask = ((-1, -1), (0, -1), (1, -1), (-1, 0), (0, 0), (1, 0), (-1, 1), (0, 1), (1, 1))

    new_lines = []

    for y in range(-1, len(lines) + 1):
        new_line = []
        new_lines.append(new_line)

        for x in range(-1, len(lines[0]) + 1):
            index_string = "".join([pixel_at(x + dx, y + dy, lines, step if algo[0] == '#' else 0) for dx, dy in pattern_mask])
            index = int(index_string, 2)

            new_line.append(algo[index])

    return new_lines


def print_lines(lines):
    for y in range(len(lines)):
        for x in range(len(lines[0])):
            if x < 0 or x >= len(lines[0]) or y < 0 or y >= len(lines):
                print(" ", end="")
            else:
                print(' ' if lines[y][x] != '#' else '\u2588', end="")
        print()
    print()


def count_lights(lines):
    count = 0
    for line in lines:
        for cell in line:
            if cell == '#':
                count += 1
    return count


def do_run(lines, steps, verbose=False):
    algo, lines = parse_input(lines)

    if verbose:
        print_lines(lines)
    for step in range(steps):
        lines = enhance(step, lines, algo)
        if verbose:
            print("At step %d" % step)
            print_lines(lines)

    return count_lights(lines)


def run():
    return do_run(from_file("inputs/20_image_enhancment"), 50)


def main():
    test(35, do_run(from_file("test_inputs/20_image_enhancment"), 2))
    test(3351, do_run(from_file("test_inputs/20_image_enhancment"), 50))
    test(5326, do_run(from_file("test_inputs/20_image_enhancment_1"), 2))
    test(5203, do_run(from_file("inputs/20_image_enhancment"), 2))
    test(18806, run())


if __name__ == '__main__':
    main()
