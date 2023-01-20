from Util import test, from_file


def parse(lines):
    return lines[0].strip().split(",")


def do_spin(programs, size):
    size = (size % len(programs))
    
    take = programs[-size:]
    stay = programs[:len(programs) - size]
    
    take.extend(stay)
    
    return take


def do_exchange(programs, source, target):
    temp = programs[source]
    programs[source] = programs[target]
    programs[target] = temp


def do_partner(programs, source, target):
    source_i = programs.index(source)
    target_i = programs.index(target)

    do_exchange(programs, source_i, target_i)


def do_move(programs, move):
    code = move[0]
    value = move[1:]

    if code == "s":
        programs = do_spin(programs, int(value))
    if code == "x":
        first, second = value.split("/")
        do_exchange(programs, int(first), int(second))
    if code == "p":
        first, second = value.split("/")
        do_partner(programs, first, second)

    return programs


def dance(programs, lines):
    programs = list(programs)
    moves = parse(lines)
    for move in moves:
        programs = do_move(programs, move)
    return "".join(programs)


def generate_programs(size):
    programs = []
    first = ord('a')
    for i in range(size):
        programs.append(chr(first + i))
    return programs


def find_repetition(programs, lines):
    visited = {}
    step = 0

    while step < 1000:
        step += 1
        programs = dance(programs, lines)
        if programs in visited:
            return step, programs
        visited[programs] = step


def dance_several(programs, lines, times):
    for i in range(times):
        programs = dance(programs, lines)
    return programs


def scaled_dance(programs, lines, all_dances):
    repetition, programs = find_repetition(programs, lines)
    actual = all_dances % repetition

    return dance_several(programs, lines, actual)


def test_repetition(size, moves, times):
    expected = dance_several(generate_programs(size), moves, times)
    actual = scaled_dance(generate_programs(size), moves, times + 1)
    test(expected, actual, "At size %d, %d steps" % (size, times))


def main():
    test_moves = from_file("test_inputs/16_dance")
    moves = from_file("inputs/16_dance")

    test("baedc", dance(generate_programs(5), test_moves))
    test("olgejankfhbmpidc", dance(generate_programs(16), moves))

    test_repetition(5, test_moves, 9)
    test_repetition(5, test_moves, 10)
    test_repetition(5, test_moves, 11)
    test_repetition(5, test_moves, 12)

    print(scaled_dance(generate_programs(16), moves, 1000000001))


if __name__ == '__main__':
    main()
