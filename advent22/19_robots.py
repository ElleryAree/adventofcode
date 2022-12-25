import re
from copy import deepcopy
from heapq import heappop, heappush
from math import floor, ceil

from Util import from_file, test

scenario_test = [
    "== Minute 1 ==",
    "1 ore-collecting robot collects 1 ore; you now have 1 ore.",
    "== Minute 2 ==",
    "1 ore-collecting robot collects 1 ore; you now have 2 ore.",
    "== Minute 3 ==",
    "Spend 2 ore to start building a clay-collecting robot.",
    "1 ore-collecting robot collects 1 ore; you now have 1 ore.",
    "The new clay-collecting robot is ready; you now have 1 of them.",
    "== Minute 4 ==",
    "1 ore-collecting robot collects 1 ore; you now have 2 ore.",
    "1 clay-collecting robot collects 1 clay; you now have 1 clay.",
    "== Minute 5 ==",
    "Spend 2 ore to start building a clay-collecting robot.",
    "1 ore-collecting robot collects 1 ore; you now have 1 ore.",
    "1 clay-collecting robot collects 1 clay; you now have 2 clay.",
    "The new clay-collecting robot is ready; you now have 2 of them.",
    "== Minute 6 ==",
    "1 ore-collecting robot collects 1 ore; you now have 2 ore.",
    "2 clay-collecting robots collect 2 clay; you now have 4 clay.",
    "== Minute 7 ==",
    "Spend 2 ore to start building a clay-collecting robot.",
    "1 ore-collecting robot collects 1 ore; you now have 1 ore.",
    "2 clay-collecting robots collect 2 clay; you now have 6 clay.",
    "The new clay-collecting robot is ready; you now have 3 of them.",
    "== Minute 8 ==",
    "1 ore-collecting robot collects 1 ore; you now have 2 ore.",
    "3 clay-collecting robots collect 3 clay; you now have 9 clay.",
    "== Minute 9 ==",
    "1 ore-collecting robot collects 1 ore; you now have 3 ore.",
    "3 clay-collecting robots collect 3 clay; you now have 12 clay.",
    "== Minute 10 ==",
    "1 ore-collecting robot collects 1 ore; you now have 4 ore.",
    "3 clay-collecting robots collect 3 clay; you now have 15 clay.",
    "== Minute 11 ==",
    "Spend 3 ore and 14 clay to start building an obsidian-collecting robot.",
    "1 ore-collecting robot collects 1 ore; you now have 2 ore.",
    "3 clay-collecting robots collect 3 clay; you now have 4 clay.",
    "The new obsidian-collecting robot is ready; you now have 1 of them.",
    "== Minute 12 ==",
    "Spend 2 ore to start building a clay-collecting robot.",
    "1 ore-collecting robot collects 1 ore; you now have 1 ore.",
    "3 clay-collecting robots collect 3 clay; you now have 7 clay.",
    "1 obsidian-collecting robot collects 1 obsidian; you now have 1 obsidian.",
    "The new clay-collecting robot is ready; you now have 4 of them.",
    "== Minute 13 ==",
    "1 ore-collecting robot collects 1 ore; you now have 2 ore.",
    "4 clay-collecting robots collect 4 clay; you now have 11 clay.",
    "1 obsidian-collecting robot collects 1 obsidian; you now have 2 obsidian.",
    "== Minute 14 ==",
    "1 ore-collecting robot collects 1 ore; you now have 3 ore.",
    "4 clay-collecting robots collect 4 clay; you now have 15 clay.",
    "1 obsidian-collecting robot collects 1 obsidian; you now have 3 obsidian.",
    "== Minute 15 ==",
    "Spend 3 ore and 14 clay to start building an obsidian-collecting robot.",
    "1 ore-collecting robot collects 1 ore; you now have 1 ore.",
    "4 clay-collecting robots collect 4 clay; you now have 5 clay.",
    "1 obsidian-collecting robot collects 1 obsidian; you now have 4 obsidian.",
    "The new obsidian-collecting robot is ready; you now have 2 of them.",
    "== Minute 16 ==",
    "1 ore-collecting robot collects 1 ore; you now have 2 ore.",
    "4 clay-collecting robots collect 4 clay; you now have 9 clay.",
    "2 obsidian-collecting robots collect 2 obsidian; you now have 6 obsidian.",
    "== Minute 17 ==",
    "1 ore-collecting robot collects 1 ore; you now have 3 ore.",
    "4 clay-collecting robots collect 4 clay; you now have 13 clay.",
    "2 obsidian-collecting robots collect 2 obsidian; you now have 8 obsidian.",
    "== Minute 18 ==",
    "Spend 2 ore and 7 obsidian to start building a geode-cracking robot.",
    "1 ore-collecting robot collects 1 ore; you now have 2 ore.",
    "4 clay-collecting robots collect 4 clay; you now have 17 clay.",
    "2 obsidian-collecting robots collect 2 obsidian; you now have 3 obsidian.",
    "The new geode-cracking robot is ready; you now have 1 of them.",
    "== Minute 19 ==",
    "1 ore-collecting robot collects 1 ore; you now have 3 ore.",
    "4 clay-collecting robots collect 4 clay; you now have 21 clay.",
    "2 obsidian-collecting robots collect 2 obsidian; you now have 5 obsidian.",
    "1 geode-cracking robot cracks 1 geode; you now have 1 open geode.",
    "== Minute 20 ==",
    "1 ore-collecting robot collects 1 ore; you now have 4 ore.",
    "4 clay-collecting robots collect 4 clay; you now have 25 clay.",
    "2 obsidian-collecting robots collect 2 obsidian; you now have 7 obsidian.",
    "1 geode-cracking robot cracks 1 geode; you now have 2 open geodes.",
    "== Minute 21 ==",
    "Spend 2 ore and 7 obsidian to start building a geode-cracking robot.",
    "1 ore-collecting robot collects 1 ore; you now have 3 ore.",
    "4 clay-collecting robots collect 4 clay; you now have 29 clay.",
    "2 obsidian-collecting robots collect 2 obsidian; you now have 2 obsidian.",
    "1 geode-cracking robot cracks 1 geode; you now have 3 open geodes.",
    "The new geode-cracking robot is ready; you now have 2 of them.",
    "== Minute 22 ==",
    "1 ore-collecting robot collects 1 ore; you now have 4 ore.",
    "4 clay-collecting robots collect 4 clay; you now have 33 clay.",
    "2 obsidian-collecting robots collect 2 obsidian; you now have 4 obsidian.",
    "2 geode-cracking robots crack 2 geodes; you now have 5 open geodes.",
    "== Minute 23 ==",
    "1 ore-collecting robot collects 1 ore; you now have 5 ore.",
    "4 clay-collecting robots collect 4 clay; you now have 37 clay.",
    "2 obsidian-collecting robots collect 2 obsidian; you now have 6 obsidian.",
    "2 geode-cracking robots crack 2 geodes; you now have 7 open geodes.",
    "== Minute 24 ==",
    "1 ore-collecting robot collects 1 ore; you now have 6 ore.",
    "4 clay-collecting robots collect 4 clay; you now have 41 clay.",
    "2 obsidian-collecting robots collect 2 obsidian; you now have 8 obsidian.",
    "2 geode-cracking robots crack 2 geodes; you now have 9 open geodes.",
]


class Blueprint:
    def __init__(self, b_id, ore, clay, obsidian, geode):
        self.b_id = b_id
        self.ore = ore
        self.clay = clay
        self.obsidian = obsidian
        self.geode = geode

    def __str__(self):
        return "Blueprint %d: ore: %d ore, clay: %d ore, obs: %d ore, %d clay, geode: %d ore, %d obs" % \
            (self.b_id, self.ore, self.clay, self.obsidian[0], self.obsidian[1], self.geode[0], self.geode[1])


class State:
    def __init__(self, ore_robots=1):
        self.time = 0

        self.ore_robots = ore_robots
        self.clay_robots = 0
        self.obsidian_robots = 0
        self.geode_robots = 0

        self.ore = 0
        self.clay = 0
        self.obsidian = 0
        self.geode = 0

        # self.resource_states = ()
        # self.robot_states = ()

        self.__order = (-self.time, self.geode, self.obsidian, self.clay, self.ore)

    def with_next_time(self, next_time):
        next_state = deepcopy(self)
        next_state.time += next_time + 1

        # next_state.resource_states = self.resource_states + (self.as_resource_tuple(), )
        # next_state.robot_states = self.robot_states + (self.as_robot_tuple(), )

        return next_state

    def collect(self):
        self.ore += self.ore_robots
        self.clay += self.clay_robots
        self.obsidian += self.obsidian_robots
        self.geode += self.geode_robots

    def __ore_score(self):
        return self.ore + self.clay * 1000 + self.obsidian * 1000000 + self.geode * 1000000000

    def as_tuple(self):
        """
        state_with(time=1, ore=1, clay=0, obsidian=0, geode=0, ore_robot=1, clay_robot=0, obsidian_robot=0, geode_robot=0),
        """
        return self.time, self.ore, self.clay, self.obsidian, self.geode, self.ore_robots, self.clay_robots, self.obsidian_robots, self.geode_robots


    def as_resource_tuple(self):
        return self.ore, self.clay, self.obsidian, self.geode

    def as_robot_tuple(self):
        return self.ore_robots, self.clay_robots, self.obsidian_robots, self.geode_robots

    def __lt__(self, other):
        if self.time < other.time:
            return True
        if self.time > other.time:
            return False

        if self.geode > other.geode:
            return True
        if self.geode < other.geode:
            return False

        if self.geode_robots > other.geode_robots:
            return True
        if self.geode_robots < other.geode_robots:
            return False

        if self.obsidian > other.obsidian:
            return True
        if self.obsidian < other.obsidian:
            return False

        if self.obsidian_robots > other.obsidian_robots:
            return True
        if self.obsidian_robots < other.obsidian_robots:
            return False

        if self.clay > other.clay:
            return True
        if self.clay < other.clay:
            return False

        if self.clay_robots > other.clay_robots:
            return True
        if self.clay_robots < other.clay_robots:
            return False

        if self.ore < other.ore:
            return True
        if self.ore > other.ore:
            return False

        return self.ore_robots < other.ore_robots

        # self_ore_score = self.__ore_score()
        # other_ore_score = other.__ore_score()
        #
        # return self_ore_score < other_ore_score

    def __str__(self):
        return "time %d. Ore: %d, clay: %d, obs: %d, geodes: %d. Robots: ore: %d, clay: %d, obs: %d, geodes: %d" % \
            (self.time, self.ore, self.clay, self.obsidian, self.geode, self.ore_robots, self.clay_robots,
             self.obsidian_robots, self.geode_robots)


line_pattern = re.compile(
    "Blueprint (\d*): Each ore robot costs (\d*) ore\. Each clay robot costs (\d*) ore\. Each obsidian robot costs (\d*) ore and (\d*) clay\. Each geode robot costs (\d*) ore and (\d*) obsidian\.")


def parse_input(lines):
    prints = []

    for line in lines:
        line = line.strip()

        match = line_pattern.match(line)
        if not match:
            print("Failed to parse line %s" % line)
            return None

        b_id = int(match.group(1))
        ore = int(match.group(2))
        clay = int(match.group(3))
        obsidian = [int(match.group(4)), int(match.group(5))]
        geode = [int(match.group(6)), int(match.group(7))]

        prints.append(Blueprint(b_id, ore, clay, obsidian, geode))

    return prints


def generate_actions(blueprint, state):
    ore = state.ore
    clay = state.clay
    obsidian = state.obsidian
    # actions = [(1, None, ore, clay, obsidian)]
    actions = []
    delayed_actions = []

    # if state.time >= 22:
    #     return [(1, None, ore, clay, obsidian)]

    if state.ore_robots < max(blueprint.clay, blueprint.obsidian[0], blueprint.geode[0]):
        if state.ore >= blueprint.ore:
            actions.append((1, "ORE", (ore + state.ore_robots) - blueprint.ore, clay + state.clay_robots, obsidian + state.obsidian_robots))
        else:
            time_to_next_ore = ceil((blueprint.ore - state.ore) / state.ore_robots)
            delayed_actions.append(
                (time_to_next_ore, "ORE",
                 (ore + (time_to_next_ore * state.ore_robots)) - blueprint.ore,
                 clay + (time_to_next_ore * state.clay_robots),
                 obsidian + (time_to_next_ore * state.obsidian_robots))
            )

    if state.clay_robots < blueprint.obsidian[1]:
        if ore >= blueprint.clay:
            actions.append((1, "CLAY", ore + state.ore_robots, clay + state.clay_robots - blueprint.clay, obsidian + state.obsidian_robots))
        elif state.ore_robots > 0:
            time_to_next_ore = ceil((blueprint.clay - state.ore) / state.ore_robots)
            delayed_actions.append(
                (time_to_next_ore, "CLAY",
                 (ore + time_to_next_ore * state.ore_robots) - blueprint.clay,
                 clay + (time_to_next_ore * state.clay_robots),
                 obsidian + (time_to_next_ore * state.obsidian_robots))
            )

    if state.obsidian_robots < blueprint.geode[1]:
        if ore >= blueprint.obsidian[0] and clay >= blueprint.obsidian[1]:
            actions.append((1, "OBSIDIAN", ore - blueprint.obsidian[0], clay - blueprint.obsidian[1], obsidian))
        elif state.ore_robots > 0 and state.clay_robots > 0:
            time_to_next_ore = ceil((blueprint.obsidian[0] - state.ore) / state.ore_robots)
            time_to_next_obs = ceil((blueprint.obsidian[1] - state.clay) / state.clay_robots)
            time_to = max(time_to_next_ore, time_to_next_obs)

            delayed_actions.append(
                (time_to, "OBSIDIAN",
                 (ore + time_to * state.ore_robots) - blueprint.obsidian[0],
                 (clay + (time_to * state.clay_robots)) - blueprint.obsidian[1],
                 obsidian + (time_to * state.obsidian_robots))
            )

    if ore >= blueprint.geode[0] and obsidian >= blueprint.geode[1]:
        actions.append((1, "GEODE", ore - blueprint.geode[0], clay, obsidian - blueprint.geode[1]))
    elif state.ore_robots > 0 and state.obsidian_robots > 0:
        time_to_next_ore = ceil((blueprint.geode[0] - state.ore) / state.ore_robots)
        time_to_next_geode = ceil((blueprint.geode[1] - state.obsidian) / state.obsidian_robots)
        time_to = max(time_to_next_ore, time_to_next_geode)

        delayed_actions.append((time_to, "GEODE",
                        (ore + time_to * state.ore_robots) - blueprint.geode[0],
                        (clay + (time_to * state.clay_robots)),
                        obsidian + (time_to * state.obsidian_robots) - blueprint.geode[1])
                       )

    if len(actions) == 0:
        delayed_actions.sort()

        delay = delayed_actions[0][0] - 1
        actions.append(
            (delay, None,
             ore + delay * state.ore_robots,
             clay + (delay * state.clay_robots),
             obsidian + (delay * state.obsidian_robots))
        )
        actions.append(delayed_actions[0])
        return actions

    actions.append((0, None, ore, clay, obsidian))
    return actions


def state_with(time, ore, clay, obsidian, geode, ore_robot, clay_robot, obsidian_robot, geode_robot):
    return time, ore, clay, obsidian, geode, ore_robot, clay_robot, obsidian_robot, geode_robot


def find(blueprint):
    frontier = [State()]
    max_geodes = 0
    visited = set()

    while len(frontier) > 0:
        # state = heappop(frontier)
        state = frontier.pop()

        """
        
        for geode robot: 
            minimal time to build: 24 - max_geods - obsidian cost
        for obisidian robot:
            miniamal time to build: 
        
        """

        tuple_state = state.as_tuple()
        if tuple_state in visited:
            continue
        visited.add(tuple_state)

        # if tuple_state in states_to_check:
            # states_to_check.remove(tuple_state)

        t = (24 - state.time)
        potential_geodes = state.geode + (state.geode_robots * t) + ((t * (t - 1)) / 2)
        if potential_geodes < max_geodes:
            continue

        # if (state.geode_robots == 0 and state.time > 24 - (blueprint.geode[1] - state.obsidian)) or\
        #         (state.obsidian_robots == 0 and state.time > 24 - (blueprint.geode[1] - state.obsidian) - (blueprint.obsidian[1] / 2 - state.clay)):
            # print("This is too late to build geode robots: %s " % state)
            # continue
        #
        # if state.geode_robots > 1:
        #     potential_geods = (24 - state.time) * state.geode_robots
        #     if potential_geods < max_geodes:
        #         # print("Pruning based on geods")
        #         continue

        if state.time >= 24:
            if state.geode > max_geodes:
                max_geodes = state.geode
                print("max geode: %d" % max_geodes)
                # print("State is %s" % str(state.as_tuple()))
            continue
            # if state.geode < max_geodes:
            #     print("Queue size %d, max geode: %d" % (len(frontier), max_geodes))
            #     break

        actions = generate_actions(blueprint, state)
        for next_time, robot, ore, clay, obsidian in actions:
            next_state = state.with_next_time(next_time)

            next_state.ore = ore
            next_state.clay = clay
            next_state.obsidian = obsidian

            next_state.collect()

            if robot == 'ORE':
                next_state.ore_robots += 1
            if robot == 'CLAY':
                next_state.clay_robots += 1
            if robot == 'OBSIDIAN':
                next_state.obsidian_robots += 1
            if robot == 'GEODE':
                next_state.geode_robots += 1

            # heappush(frontier, next_state)
            frontier.append(next_state)

    # if len(states_to_check) != 0:
    #     for state in sorted(states_to_check):
    #         print(state)

    return max_geodes


def find_ore(blueprint):
    frontier = [State()]
    max_ore = 0
    visited = set()

    step_to_ore = {}

    weird_map = {}

    while len(frontier) > 0:
        state = heappop(frontier)

        tuple_state = state.as_tuple()
        if tuple_state in visited:
            continue
        visited.add(tuple_state)

        robots_by_ore = weird_map.get(state.time)
        if robots_by_ore is None:
            robots_by_ore = {}
            weird_map[state.time] = robots_by_ore

        time_by_robots = robots_by_ore.get(state.ore_robots)
        if time_by_robots is None:
            time_by_robots = set()
            robots_by_ore[state.ore_robots] = time_by_robots
        time_by_robots.add(state.ore)

        max_at_step = step_to_ore.get(state.time, 0)
        if state.ore > max_at_step:
            step_to_ore[state.time] = state.ore

        if state.time >= 24:
            if state.ore > max_ore:
                max_ore = state.ore
            continue

        actions = generate_actions(blueprint, ((), state.ore, state.clay, state.obsidian), allow_ore=True, allow_clay=False,
                                   allow_obsidian=False, allow_geode=False)
        for robots, ore, clay, obsidian in actions:
            next_state = state.with_next_time()

            next_state.ore = ore
            next_state.clay = clay
            next_state.obsidian = obsidian

            next_state.collect()

            for robot in robots:
                if robot == 'ORE':
                    next_state.ore_robots += 1
                if robot == 'CLAY':
                    next_state.clay_robots += 1
                if robot == 'OBSIDIAN':
                    next_state.obsidian_robots += 1
                if robot == 'GEODE':
                    next_state.geode_robots += 1

            heappush(frontier, next_state)

    # for time, ore in sorted(step_to_ore.items()):
    #     print("At step %s max ore is %d" % (time, ore))

    for time, robots_by_ore in sorted(weird_map.items()):
        print("Time: %d" % time)
        print("Could have by now: %d" % (int((time + 1) / 4)))
        for robots, time_by_robots in sorted(robots_by_ore.items()):
            # print("-- Robots: %d: Ore: %s" % (robots, ", ".join(map(str, sorted(time_by_robots)))))
            print("-- Robots: %d: Ore: %s" % (robots, max(time_by_robots)))

    return max_ore


def find_clay(blueprint):
    frontier = [State()]
    max_ore = 0
    visited = set()

    step_to_ore = {}

    weird_map = {}

    while len(frontier) > 0:
        state = heappop(frontier)

        tuple_state = state.as_tuple()
        if tuple_state in visited:
            continue
        visited.add(tuple_state)

        robots_by_ore = weird_map.get(state.time)
        if robots_by_ore is None:
            robots_by_ore = {}
            weird_map[state.time] = robots_by_ore

        time_by_robots = robots_by_ore.get(state.clay_robots)
        if time_by_robots is None:
            time_by_robots = set()
            robots_by_ore[state.clay_robots] = time_by_robots
        time_by_robots.add(state.clay)

        max_at_step = step_to_ore.get(state.time, 0)
        if state.clay > max_at_step:
            step_to_ore[state.time] = state.clay

        if state.time >= 24:
            if state.ore > max_ore:
                max_ore = state.ore
            continue

        actions = generate_actions(blueprint, ((), state.ore, state.clay, state.obsidian), allow_ore=False,
                                   allow_obsidian=False, allow_geode=False)
        for robots, ore, clay, obsidian in actions:
            next_state = state.with_next_time()

            next_state.ore = ore
            next_state.clay = clay
            next_state.obsidian = obsidian

            next_state.collect()

            for robot in robots:
                if robot == 'ORE':
                    next_state.ore_robots += 1
                if robot == 'CLAY':
                    next_state.clay_robots += 1
                if robot == 'OBSIDIAN':
                    next_state.obsidian_robots += 1
                if robot == 'GEODE':
                    next_state.geode_robots += 1

            heappush(frontier, next_state)

    # for time, ore in sorted(step_to_ore.items()):
    #     print("At step %s max ore is %d" % (time, ore))

    for ore, robots_by_ore in sorted(weird_map.items()):
        print("Time: %d" % ore)
        for robots, time_by_robots in sorted(robots_by_ore.items()):
            # print("-- Robots: %d: Clay: %s" % (robots, ", ".join(map(str, sorted(time_by_robots)))))
            print("-- Robots: %d: Clay: %s" % (robots, max(time_by_robots)))

    return max_ore


def find_ore_from_example(lines):
    minutes_pattern = re.compile("== Minute (\d*) ==")
    ore_pattern = re.compile(".*collect(?:s|) (\d*) ore.*")
    clay_pattern = re.compile(".*collect(?:s|) (\d*) clay.*")
    obsidian_pattern = re.compile(".*collect(?:s|) (\d*) obsidian.*")
    geode_pattern = re.compile(".*crack(?:s|) (\d*) geode.*")

    total_ore = 0
    total_clay = 0
    total_obsidian = 0
    total_geodes = 0

    for line in lines:
        # minutes_match = minutes_pattern.match(line)
        # if minutes_match:
        #     print(line)

        match = ore_pattern.match(line)
        if match:
            total_ore += int(match.group(1))

        match = clay_pattern.match(line)
        if match:
            total_clay += int(match.group(1))

        match = obsidian_pattern.match(line)
        if match:
            total_obsidian += int(match.group(1))

        match = geode_pattern.match(line)
        if match:
            total_geodes += int(match.group(1))

    print("During example robots collected:")
    print(" -      Ore: %d" % total_ore)
    print(" -     Clay: %d" % total_clay)
    print(" - Obsidian: %d" % total_obsidian)
    print(" -   Geodes: %d" % total_geodes)



def find_all(prints):
    total = 0

    for blueprint in prints:
        geodes = find(blueprint)
        print("For blueprint %d, max is %d" % (blueprint.b_id, geodes))
        total += blueprint.b_id * geodes

    return total


def main():
    """
    During example robots collected:
     -      Ore: 24
     -     Clay: 69
     - Obsidian: 22
     -   Geodes: 9
    """

    # find_ore(parse_input(from_file("test_inputs/19_robots"))[0])
    # find_clay(parse_input(from_file("test_inputs/19_robots"))[0])
    # find_ore_from_example(scenario_test)

    test(9, find(parse_input(from_file("test_inputs/19_robots"))[0]))
    # test(12, find(parse_input(from_file("test_inputs/19_robots"))[1]))
    # test(33, find_all(parse_input(from_file("test_inputs/19_robots"))))
    # find(parse_input(from_file("inputs/19_robots")))

    # answer = find_all(parse_input(from_file("inputs/19_robots")))
    # test(1186, answer, "1186 is too low", lambda a, e: a > e)
    # print(answer)


if __name__ == '__main__':
    main()


"""

geode: 2 ore, 7 obsidian




"""


