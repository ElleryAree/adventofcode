from collections import deque

from Util import test, from_file


class Basic:
    def __init__(self, name, match):
        self.__name = name
        self.__match = match

    def check(self, line, start) -> list:
        try:
            return [start + 1] if start < len(line) and line[start] == self.__match else []
        except IndexError as err:
            print("Failed on rule %s on line: %s (%d), start: %s" % (self.__name, line, len(line), start))
            raise err

    def __str__(self):
        return self.__name


class SubRule:
    def __init__(self, name, or_rules, rules_map):
        self.__name = name
        self.__or_rules = or_rules
        self.__rules_map = rules_map

    def check(self, line, start) -> list:
        valid = []
        for rules in self.__or_rules:
            check_res = self.__check_rules(line, rules, start)
            valid.extend(check_res)

        return valid

    def __check_rules(self, line, rules, start) -> list:
        queue = deque()
        queue.append((0, start))

        valid = []
        while len(queue) > 0:
            i, start = queue.pop()
            rule = self.__rules_map[rules[i]]

            matches = rule.check(line, start)
            for match in matches:
                if i >= len(rules) - 1:
                    valid.append(match)
                else:
                    queue.append((i + 1, match))

        return valid

    def __str__(self):
        return self.__name


def validate_rule(line, rules_map):
    queue = deque()
    cache = {}

    queue.append((0, ("0", )))

    while len(queue) > 0:
        entry = queue.pop()
        cached = cache.get(entry, None)


def parse_line(line, rules_map):
    rule_id, body = line.split(": ")

    if '"' in body:
        rule = Basic(line, body.strip()[1:-1])
        rules_map[rule_id] = rule
        return

    or_parts = body.split(" | ")

    rule = SubRule(line, list(map(lambda rule: rule.split(" "), or_parts)), rules_map)
    rules_map[rule_id] = rule


def identity(rules_map):
    pass


def parse_input(lines, update=identity):
    rules_map = {}
    rules_filled = False
    matches = 0

    for line in lines:
        line = line.strip()
        if line == "":
            update(rules_map)
            rules_filled = True
            continue

        if not rules_filled:
            parse_line(line, rules_map)
        else:
            valid_lens = rules_map['0'].check(line, 0)
            if any(map(lambda valid_len: valid_len == len(line), valid_lens)):
                matches += 1

    return matches


def change_rules(rules_map):
    parse_line("8: 42 | 42 8", rules_map)
    parse_line("11: 42 31 | 42 11 31", rules_map)


def run():
    return parse_input(from_file("inputs/19_rules"), change_rules)


if __name__ == '__main__':
    test_input = ["0: 4 1 5\n", "1: 2 3 | 3 2\n", "2: 4 4 | 5 5\n", "3: 4 5 | 5 4\n", '4: "a"\n', '5: "b"\n', "\n", "ababbb\n", "bababa\n", "abbbab\n", "aaabbb\n", "aaaabbb\n"]
    test_input_2 = ['42: 9 14 | 10 1\n', '9: 14 27 | 1 26\n', '10: 23 14 | 28 1\n', '1: "a"\n', '11: 42 31\n', '5: 1 14 | 15 1\n', '19: 14 1 | 14 14\n', '12: 24 14 | 19 1\n', '16: 15 1 | 14 14\n', '31: 14 17 | 1 13\n', '6: 14 14 | 1 14\n', '2: 1 24 | 14 4\n', '0: 8 11\n', '13: 14 3 | 1 12\n', '15: 1 | 14\n', '17: 14 2 | 1 7\n', '23: 25 1 | 22 14\n', '28: 16 1\n', '4: 1 1\n', '20: 14 14 | 1 15\n', '3: 5 14 | 16 1\n', '27: 1 6 | 14 18\n', '14: "b"\n', '21: 14 1 | 1 14\n', '25: 1 1 | 1 14\n', '22: 14 14\n', '8: 42\n', '26: 14 22 | 1 20\n', '18: 15 15\n', '7: 14 5 | 1 21\n', '24: 14 1\n', ' \n', 'abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa\n', 'bbabbbbaabaabba\n', 'babbbbaabbbbbabbbbbbaabaaabaaa\n', 'aaabbbbbbaaaabaababaabababbabaaabbababababaaa\n', 'bbbbbbbaaaabbbbaaabbabaaa\n', 'bbbababbbbaaaaaaaabbababaaababaabab\n', 'ababaaaaaabaaab\n', 'ababaaaaabbbaba\n', 'baabbaaaabbaaaababbaababb\n', 'abbbbabbbbaaaababbbbbbaaaababb\n', 'aaaaabbaabaaaaababaa\n', 'aaaabbaaaabbaaa\n', 'aaaabbaabbaaaaaaabbbabbbaaabbaabaaa\n', 'babaaabbbaaabaababbaabababaaab\n', 'aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba\n']

    test(2, parse_input(test_input))
    test(3, parse_input(test_input_2))
    test(12, parse_input(test_input_2, change_rules))

    print(run())
