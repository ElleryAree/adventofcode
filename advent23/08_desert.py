from Util import test, from_file


def parse(lines):
    turns = lines.pop(0).strip()
    lines.pop(0)

    path = {}
    for line in lines:
        name, next_locs = line.strip().split(" = ")
        locs = next_locs[1:-1].split(", ")
        path[name] = locs

    return turns, path


def follow_the_path(turns, path):
    count = 0
    loc = 'AAA'

    turn_id = 0

    while loc != 'ZZZ':
        turn = turns[turn_id]
        turn_id += 1
        count += 1
        if turn_id >= len(turns):
            turn_id = 0

        next_locs = path[loc]
        next_loc_id = 1 if turn == 'R' else 0
        loc = next_locs[next_loc_id]

    return count


def find_all_exits(enter, turns, path):
    count = 0

    visited = set()
    loc = enter

    exits = []

    turn_id = 0

    while (turn_id, loc) not in visited:
        visited.add((turn_id, loc))
        if loc[-1] == 'Z':
            exits.append(count)

        count += 1

        turn = turns[turn_id]
        turn_id += 1
        if turn_id >= len(turns):
            turn_id = 0

        next_locs = path[loc]
        next_loc_id = 1 if turn == 'R' else 0
        loc = next_locs[next_loc_id]

    return exits


def find_all_exits_for_all_enters(turns, path):
    all_exits = []
    for enter in filter(lambda loc: loc[-1] == 'A', path):
        exits = find_all_exits(enter, turns, path)
        all_exits.append(exits)

    return all_exits


def find_intersection(all_exits):
    only_exit = [exits[0] for exits in all_exits]
    only_exit.sort()

    period = only_exit.pop()
    while len(only_exit) > 0:
        mult = 1
        next_period = only_exit.pop()

        while (period * mult) % next_period != 0:
            mult += 1

        period *= mult

    return period


def part_1(lines):
    turns, path = parse(lines)
    return follow_the_path(turns, path)


def part_2(lines):
    turns, path = parse(lines)
    all_exits = find_all_exits_for_all_enters(turns, path)
    return find_intersection(all_exits)


def run():
    print(part_2(from_file("inputs/08_desert")))


def main():
    test(2, part_1(from_file("test_inputs/08_desert")))
    test(14257, part_1(from_file("inputs/08_desert")))

    test(6, part_2(from_file("test_inputs/08_desert_part_2")))
    run()


if __name__ == '__main__':
    main()
