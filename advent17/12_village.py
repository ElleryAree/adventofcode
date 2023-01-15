from Util import test, from_file


class Program:
    def __init__(self, name, comms):
        self.name = name
        self.comms = comms


def parse_input(lines):
    programs = {}

    for line in lines:
        line = line.strip()

        name, comms = line.split(" <-> ")
        prog = Program(name, comms.split(", "))
        programs[name] = prog

    return programs


def find_accessebles(start, progs):
    frontier = [start]
    visited = set()

    while len(frontier) > 0:
        name = frontier.pop()

        if name in visited:
            continue
        visited.add(name)

        prog = progs[name]
        frontier.extend(prog.comms)

    return visited


def part_1(lines):
    return len(find_accessebles("0", parse_input(lines)))


def part_2(lines):
    progs = parse_input(lines)
    total_visited = set()
    groups = 0

    for prog in progs:
        if prog in total_visited:
            continue

        visited = find_accessebles(prog, progs)

        groups += 1
        total_visited.update(visited)

    return groups



def main():
    test(6, part_1(from_file("test_inputs/12_village")))
    test(134, part_1(from_file("inputs/12_village")))

    test(2, part_2(from_file("test_inputs/12_village")))
    print(part_2(from_file("inputs/12_village")))


if __name__ == '__main__':
    main()
