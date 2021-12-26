from Util import test, from_file


def parse_command(input: str, state: (int, int, int)):
    command, value = input.strip().split(" ")
    value = int(value)

    horizontal, depth, aim = state
    if command == 'forward':
        return horizontal + value, depth + (aim * value), aim
    elif command == 'down':
        return horizontal, depth, aim + value
    elif command == 'up':
        return horizontal, depth, aim - value
    else:
        return state


def run_all(commands):
    state = (0, 0, 0)

    for command in commands:
        state = parse_command(command, state)

    return state[0] * state[1]


def run():
    return run_all(from_file("inputs/02_course"))


def main():
    test(900, run_all(("forward 5", "down 5", "forward 8", "up 3", "down 8", "forward 2")))
    print(run())


if __name__ == '__main__':
    main()
