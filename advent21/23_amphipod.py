from heapq import heappop, heappush

from Util import from_file, test


def get_energy(amphipod):
    if amphipod == 'A':
        return 1
    if amphipod == 'B':
        return 10
    if amphipod == 'C':
        return 100
    if amphipod == 'D':
        return 1000


def destination(amphipod):
    if amphipod == 'A':
        return 3
    if amphipod == 'B':
        return 5
    if amphipod == 'C':
        return 7
    if amphipod == 'D':
        return 9


def rooms_are_correct(amphipod, other_amphs, x, start_y):
    for y in range(start_y, 6):
        cell = is_occupied(other_amphs, x, y)

        if cell != '.' and cell != amphipod:
            return False

    return True


def can_stop(amphipod, other_amphs, x, y, start_x, start_y):
    if x == start_x and y == start_y:
        return False

    if start_y == 1:
        if y > 1 and x == destination(amphipod):
            if y == 2:
                if not is_occupied_all(amphipod, other_amphs, x, 3):
                    return False
            if y == 3:
                if not is_occupied_all(amphipod, other_amphs, x, 4):
                    return False
            if y == 4:
                if not is_occupied_all(amphipod, other_amphs, x, 5):
                    return False

            return True
        return False

    if y == 1 and x in (3, 5, 7, 9):
        return False

    if y > 1:
        return x == destination(amphipod) and rooms_are_correct(amphipod, other_amphs, x, y)

    return True


def is_occupied_all(amphipod, other_amphs, x_dx, y_dy):
    for y in range(y_dy, 6):
        if is_occupied(other_amphs, x_dx, y) != amphipod:
            return False
    return True


def is_occupied(other_amphs, x_dx, y_dy):
    for pod, x, y in other_amphs:
        if x == x_dx and y == y_dy:
            return pod
    return '.'


def find_all_targets(burrow, amphipod, other_amphs, start_x, start_y, energy):
    queue = [(energy, (start_x, start_y))]
    visited = set()

    possible_targets = []

    while len(queue) > 0:
        energy, pos = queue.pop()
        if pos in visited:
            continue
        visited.add(pos)

        x, y = pos

        if can_stop(amphipod, other_amphs, x, y, start_x, start_y):
            possible_targets.append((energy, pos))

        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            y_dy = y + dy
            x_dx = x + dx
            cell = burrow[y_dy][x_dx]

            if cell != '.' or is_occupied(other_amphs, x_dx, y_dy) != '.':
                continue

            queue.append((energy + get_energy(amphipod), (x_dx, y_dy)))

    return possible_targets


def distance_to_target(amphipods_state):
    distance = 0
    for amphipod, x, y in amphipods_state:
        dest_x = destination(amphipod)

        if y > 1 and x == dest_x:
            continue

        if y == 1:
            distance += abs(x - dest_x) + 1
        else:
            distance += abs(x - dest_x) + 1 + (y - 1)

    return distance


def find_all_actions(burrow, amphipods_state, starting_energy, history):
    actions = []

    for i in range(len(amphipods_state)):
        amphipod_state = amphipods_state[i]
        other_pods = tuple(filter(lambda other: other != amphipod_state, amphipods_state))

        amphipod, x, y = amphipod_state

        if x == x == destination(amphipod):
            if y == 5:
                continue
            if y == 4 and rooms_are_correct(amphipod, other_pods, x, 4):
                continue
            if y == 3 and rooms_are_correct(amphipod, other_pods, x, 3):
                continue
            if y == 2 and rooms_are_correct(amphipod, other_pods, x, 2):
                continue

        for energy, (next_x, next_y) in find_all_targets(burrow, amphipod, other_pods, x, y, starting_energy):
            next_state = tuple(sorted(other_pods + ((amphipod, next_x, next_y), )))
            next_history = history + ("%s (%s, %s) -> (%s, %s)" % (amphipod, x, y, next_x, next_y), )
            actions.append((energy, next_state, next_history))

    return actions


def locate_amphipods(burrow):
    amphipods = []
    for y, line in enumerate(burrow):
        for x, cell in enumerate(line):
            if cell in ('A', 'B', "C", 'D'):
                amphipods.append((cell, x, y))
                line[x] = '.'

    return amphipods


def is_goal(amphipods_state):
    return ("A", 3, 2) in amphipods_state and \
            ("A", 3, 3) in amphipods_state and \
            ("A", 3, 4) in amphipods_state and \
            ("A", 3, 5) in amphipods_state and \
            ("B", 5, 2) in amphipods_state and \
            ("B", 5, 3) in amphipods_state and \
            ("B", 5, 4) in amphipods_state and \
            ("B", 5, 5) in amphipods_state and \
            ("C", 7, 2) in amphipods_state and \
            ("C", 7, 3) in amphipods_state and \
            ("C", 7, 4) in amphipods_state and \
            ("C", 7, 5) in amphipods_state and \
            ("D", 9, 2) in amphipods_state and \
            ("D", 9, 3) in amphipods_state and \
            ("D", 9, 4) in amphipods_state and \
            ("D", 9, 5) in amphipods_state


def find_alignment(burrow):
    burrow = list(map(list, burrow))
    amphipods = locate_amphipods(burrow)

    queue = [(0, tuple(amphipods), ())]
    visited = set()

    step = 0

    while len(queue) > 0:
        step += 1
        energy, amphipods_state, history = heappop(queue)

        if amphipods_state in visited:
            continue

        if is_goal(amphipods_state):
            return energy

        visited.add(amphipods_state)

        for action in find_all_actions(burrow, amphipods_state, energy, history):
            heappush(queue, action)


def run():
    return find_alignment(from_file("inputs/23_amphipod"))


def main():
    test(44169, find_alignment(from_file("test_inputs/23_amphipod")))
    test(48984, run())


if __name__ == '__main__':
    main()
