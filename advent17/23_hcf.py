from Util import from_file, test


def is_prime(n):
    if n == 2 or n == 3:
        return True
    if n % 2 == 0 or n < 2:
        return False

    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            return False

    return True


def program_decompiles(is_debug):
    start = 84
    stop = start
    prime_count = 0

    if not is_debug:
        start = start * 100 + 100000
        stop = start + 17000

    for i in range(start, stop + 17, 17):
        if not is_prime(i):
            prime_count += 1

    return prime_count


def parse_lines(lines):
    return list(map(lambda line: line.strip().split(" "), lines))


def number_or_register(value, registers):
    register = registers.get(value)
    return register if register is not None else int(value)


def execute(value_a, lines):
    lines = parse_lines(lines)

    registers = {}
    for i in range(ord('a'), ord('h') + 1):
        registers[chr(i)] = 0

    registers['a'] = value_a
    registers['m'] = 0

    instruction = 0

    while instruction < len(lines):
        inc = 1
        parts = lines[instruction]
        register = number_or_register(parts[1], registers)

        if parts[0] == "set":
            registers[parts[1]] = number_or_register(parts[2], registers)
        elif parts[0] == "sub":
            registers[parts[1]] = register - number_or_register(parts[2], registers)
        elif parts[0] == "mul":
            registers['m'] += 1
            registers[parts[1]] = register * number_or_register(parts[2], registers)
        elif parts[0] == "jnz" and register != 0:
            inc = number_or_register(parts[2], registers)

        instruction += inc

    return registers


def main():
    test(6724, execute(0, from_file("inputs/23_hcf"))['m'])
    test(903, program_decompiles(False))


if __name__ == '__main__':
    main()
