from Util import test, from_file


def part_1(offset):
    return offset + 1


def part_2(offset):
    return offset - 1 if offset >= 3 else offset + 1


def follow_maze(maze, f):
    i = 0
    steps = 0

    while 0 <= i < len(maze):
        steps += 1
        instruction = maze[i]
        maze[i] = f(instruction)
        i += instruction

    return steps


def parse_and_follow(lines, f):
    return follow_maze(list(map(lambda line: int(line.strip()), lines)), f)


def main():
    test(5, parse_and_follow(from_file("test_inputs/05_maze"), part_1))
    test(326618, parse_and_follow(from_file("inputs/05_maze"), part_1))

    test(10, parse_and_follow(from_file("test_inputs/05_maze"), part_2))
    print(parse_and_follow(from_file("inputs/05_maze"), part_2))


if __name__ == '__main__':
    main()
