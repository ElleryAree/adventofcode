from collections import deque
from re import compile

from Util import test, from_file

rule_pattern = compile("([a-zA-Z\\s]*): (\\d*)-(\\d*) or (\\d*)-(\\d*)")


def parse_rules(lines):
    rules = []

    for i, line in enumerate(lines):
        line = line.strip()

        if line == "":
            return i, rules

        match = rule_pattern.match(line)
        if not match:
            raise Exception("%s is not a rule" % line)

        name = match.group(1)
        low_1 = int(match.group(2))
        high_1 = int(match.group(3))
        low_2 = int(match.group(4))
        high_2 = int(match.group(5))

        rules.append(Rule(name, low_1, high_1, low_2, high_2))


def parse_ticket(line):
    return list(map(int, line.strip().split(",")))


def parse_input(lines):
    next_i, rules = parse_rules(lines)

    my_ticket = parse_ticket(lines[next_i + 2])

    other_tickets = []

    for i in range(next_i + 5, len(lines)):
        numbers = parse_ticket(lines[i])
        other_tickets.append(numbers)

    return rules, my_ticket, other_tickets


def check_number(number, rules):
    for rule in rules:
        if rule.is_valid(number):
            return True

    return False


def validate_ticket(rules, ticket):
    for number in ticket:
        if not check_number(number, rules):
            return number


def validate_all_tickets(rules, other_tickets):
    sum = 0

    for ticket in other_tickets:
        bad_number = validate_ticket(rules, ticket)
        if bad_number is not None:
            sum += bad_number

    return sum


def filter_tickets(rules, other_tickets):
    filtered = []

    for ticket in other_tickets:
        if validate_ticket(rules, ticket) is None:
            filtered.append(ticket)

    return filtered


def is_applicable(column, rule, tickets):
    for ticket in tickets:
        if not rule.is_valid(ticket[column]):
            return False
    return True


def build_domain(rules, other_tickets):
    domain = []
    for i in range(len(other_tickets[0])):
        possible_rules = []
        for j, rule in enumerate(rules):
            if is_applicable(i, rule, other_tickets):
                possible_rules.append(j)

        domain.append(possible_rules)

    return domain


def clean_domain(domain):
    queue = deque()
    visited = set()
    for i, option in enumerate(domain):
        if len(option) == 1:
            queue.append((i, option[0]))
            break

    while len(queue) > 0:
        single_i, single_option = queue.pop()
        visited.add((single_i, single_option))

        for i, option in enumerate(domain):
            if i == single_i:
                continue

            if single_option in option:
                option.remove(single_option)

            if len(option) == 0:
                return None

            if len(option) == 1 and (i, option[0]) not in visited:
                queue.append((i, option[0]))

    return domain


def is_departures(rule):
    departure_name = 'departure'
    dep_len = len(departure_name)

    return rule.name[:dep_len] == departure_name


def calculate_departures(my_ticket, domain, rules):
    total = 1
    for i, option in enumerate(domain):
        rule = rules[option[0]]

        if not is_departures(rule):
            continue

        total *= my_ticket[i]

    return total


def solve_tickets(rules, my_ticket, other_tickets):
    other_tickets = filter_tickets(rules, other_tickets)

    domain = build_domain(rules, other_tickets)
    clean_domain(domain)

    return calculate_departures(my_ticket, domain, rules)


def run_lines(lines, f):
    rules, my_ticket, other_tickets = parse_input(lines)

    return f(rules, my_ticket, other_tickets)


class Rule:
    def __init__(self, name, low_1, high_1, low_2, high_2):
        self.name = name
        self.__low_1 = low_1
        self.__high_1 = high_1
        self.__low_2 = low_2
        self.__high_2 = high_2

    def is_valid(self, number):
        return self.__low_1 <= number <= self.__high_1 or self.__low_2 <= number <= self.__high_2

    def __str__(self):
        return "%s: %d - %d or %d - %d" % (self.name, self.__low_1, self.__high_1, self.__low_2, self.__high_2)


def run():
    return run_lines(from_file("inputs/16_rules"), solve_tickets)


if __name__ == '__main__':
    test_input = ["class: 1-3 or 5-7\n", "row: 6-11 or 33-44\n", "seat: 13-40 or 45-50\n", "\n", "your ticket:\n",
                  "7,1,14\n", "\n", "nearby tickets:\n", "7,3,47\n", "40,4,50\n", "55,2,20\n", "38,6,12\n"]

    test_input_2 = ["class: 0-1 or 4-19\n", "row: 0-5 or 8-19\n", "seat: 0-13 or 16-19\n", "\n", "your ticket:\n",
                  "11,12,13\n", "\n", "nearby tickets:\n", "3,9,18\n", "15,1,5\n", "5,14,9\n"]

    # test(71, run(test_input, lambda r, _, o: validate_all_tickets(r, o)))
    # test(27911, run(from_file("inputs/16_rules"), lambda r, _, o: validate_all_tickets(r, o)))

    # run(test_input_2, solve_tickets)
    print(run())
