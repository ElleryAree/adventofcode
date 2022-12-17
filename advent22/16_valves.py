import re
from heapq import heappop, heappush

from Util import from_file, test


line_pattern = re.compile("Valve ([A-Z]{2}) has flow rate=(\d*); tunnel(?:s|) lead(?:s|) to valve(?:s|) (.*)")


class State:
    def __init__(self, released, time, name, open_vs):
        self.released = released
        self.time = time
        self.name = name
        self.open_vs = open_vs

    def __lt__(self, other):
        if self.time > other.time:
            return True
        if self.time < other.time:
            return False

        return self.released > other.released

    def __str__(self):
        return "released: %s,  time: %s, name: %s, open: %s" % (-self.released, self.time, self.name, self.open_vs)


class StateWithElephant:
    def __init__(self, released, time, hero_name, elephant_name, open_vs, operational):
        self.released = released
        self.time = time
        self.hero_name = hero_name
        self.elephant_name = elephant_name
        self.open_vs = open_vs
        self.operational = operational

    def __lt__(self, other):
        return self.time - self.operational > other.time - other.operational

    def __str__(self):
        return "released: %s,  time: %s, h_name: %s, e_name %s, open: %s" % (self.released, self.time, self.hero_name, self.elephant_name, self.open_vs)


class Valve:
    def __init__(self, name, rate, paths):
        self.name = name
        self.rate = rate
        self.paths = paths

    def __str__(self):
        return "Valve %s has flow rate=%d; tunnels lead to valves %s" % (self.name, self.rate, self.paths)


def parse_input(lines):
    valves = {}
    operational = []

    for line in lines:
        match = line_pattern.match(line.strip())
        if match is None:
            print("Failed to parse line %s" % line)
            return

        name = match.group(1)
        rate = int(match.group(2))
        paths = tuple(match.group(3).split(", "))

        if rate > 0:
            operational.append(name)

        valves[name] = Valve(name, rate, paths)

    return valves, operational


def find_path(valves):
    valves, _ = valves
    frontier = [State(0, 30, 'AA', ())]
    visited = set()
    best_pressure = 0

    while len(frontier) > 0:
        state = heappop(frontier)
        state_v = (state.name, state.released)
        if state_v in visited or state.time == 0:
            if state.released < best_pressure:
                best_pressure = state.released
            continue

        visited.add(state_v)

        valve = valves[state.name]
        time = state.time
        released = state.released
        open_vs = state.open_vs

        # actions open:
        if state.name not in open_vs and valve.rate > 0:
            # next_path = state.path[:-1] + (state.name.lower(),)
            heappush(frontier, State(released - valve.rate * (time - 1), time - 1, state.name, open_vs + (state.name,)))

        # actions GO
        for next_valve in valve.paths:
            # next_path = state.path + (next_valve, )
            heappush(frontier, State(released, time - 1, next_valve, open_vs))

    return -best_pressure


def find_path_with_elephant(valves):
    valves, operational = valves

    frontier = [StateWithElephant(0, 26, 'AA', 'AA', (), len(operational))]
    visited = set()
    best_pressure = 0

    while len(frontier) > 0:
        state = heappop(frontier)
        state_v = (min(state.hero_name, state.elephant_name), max(state.hero_name, state.elephant_name), state.released)

        if state_v in visited:
            continue

        if state.time == 0 or state.operational == 0:
            if state.released >= best_pressure:
                best_pressure = state.released
                continue
            elif best_pressure - state.released > 1000:
                break

        visited.add(state_v)

        time = state.time
        released = state.released
        open_vs = state.open_vs

        hero_name = state.hero_name
        elephant_name = state.elephant_name

        hero_valve = valves[hero_name]
        elephant_valve = valves[elephant_name]

        hero_can_open = hero_name not in open_vs and hero_valve.rate > 0
        elephant_can_open = elephant_name not in open_vs and elephant_valve.rate > 0

        # Options:
        # hero opens, elephant moves
        if hero_can_open:
            next_open_vs = open_vs + (hero_name,)

            for next_valve in elephant_valve.paths:
                next_state = StateWithElephant(released + hero_valve.rate * (time - 1), time - 1, hero_name, next_valve, next_open_vs, state.operational - 1)

                heappush(frontier, next_state)

        # elephant opens, hero moves
        if elephant_can_open:
            next_open_vs = open_vs + (elephant_name,)

            for next_valve in hero_valve.paths:
                next_state = StateWithElephant(released + elephant_valve.rate * (time - 1), time - 1, next_valve, elephant_name, next_open_vs, state.operational - 1)

                heappush(frontier, next_state)

        # both opens
        if hero_can_open and elephant_can_open and hero_name != elephant_name:
            next_open_vs = open_vs + (hero_name, elephant_name)

            next_released = released + hero_valve.rate * (time - 1) + elephant_valve.rate * (time - 1)

            next_state = StateWithElephant(next_released, time - 1, hero_name, elephant_name, next_open_vs, state.operational - 2)
            heappush(frontier, next_state)

        # both moves
        for h_name in hero_valve.paths:
            for e_name in elephant_valve.paths:
                if h_name == e_name:
                    continue
                heappush(frontier, StateWithElephant(released, time - 1, h_name, e_name, open_vs, state.operational))

    return best_pressure


def run():
    return find_path_with_elephant(parse_input(from_file("inputs/16_valves")))


def main():
    test(1651, find_path(parse_input(from_file("test_inputs/16_valves"))))
    test(2114, find_path(parse_input(from_file("inputs/16_valves"))))
    test(1707, find_path_with_elephant(parse_input(from_file("test_inputs/16_valves"))))

    print(run())


if __name__ == '__main__':
    main()
