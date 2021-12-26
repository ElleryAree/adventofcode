from copy import copy, deepcopy
from heapq import heappop, heappush

from Util import test, from_file


class Domain:
    def __init__(self, main_digs_domain, sign_digs_domain, from_domain=None):
        self.main_digs_domain = main_digs_domain
        self.sign_digs_domain = sign_digs_domain

        if from_domain is None:
            self.__domain = {c: ['a', 'b', 'c', 'd', 'e', 'f', 'g'] for c in ['a', 'b', 'c', 'd', 'e', 'f', 'g']}
        else:
            self.__domain = from_domain

    def map(self, segments):
        mapped = []
        for c in segments:
            mapped.append(self.__domain[c][0])
        return "".join(sorted(mapped))

    def update(self, new_domains):
        for letter, new_domain in new_domains.items():
            updated_domain = list(filter(lambda l: l in new_domain, self.__domain[letter]))
            self.__domain[letter] = updated_domain

        letters_to_remove = ()
        for domains in new_domains.values():
            letters_to_remove = domains
            break

        for letter, letter_domain in self.__domain.items():
            if letter in new_domains:
                continue

            for to_remove in letters_to_remove:
                if to_remove in letter_domain:
                    letter_domain.remove(to_remove)

    def digit_actions(self):
        actions = []

        for segment, digits in self.main_digs_domain:
            for digit in digits:
                domain_copy = list(filter(lambda p: p != (segment, digits), self.main_digs_domain))
                domain_copy.append((segment, [digit]))

                action = Domain(domain_copy, deepcopy(self.sign_digs_domain), deepcopy(self.__domain))
                actions.append(action)

        for segment, digits in self.sign_digs_domain:
            for digit in digits:
                domain_copy = list(filter(lambda p: p != (segment, digits), self.sign_digs_domain))
                domain_copy.append((segment, [digit]))

                action = Domain(self.main_digs_domain, domain_copy, deepcopy(self.__domain))
                actions.append(action)

        return actions

    def run_domain(self):
        segment_and_digits = copy(self.main_digs_domain)
        segment_and_digits.extend(self.sign_digs_domain)

        for segment, digits in segment_and_digits:
            if len(digits) > 1 or digits[0] == 8:
                continue

            new_domain = all_segments_domain(segment, digits[0])
            self.update(new_domain)

    def is_valid(self):
        for options in self.__domain.values():
            if len(options) == 0:
                return False
        return True

    def is_goal(self):
        return all(map(lambda opt: len(opt) == 1, self.__domain.values()))

    def to_string(self):
        return ",".join(map(lambda p: "{%s:[%s]}" % (p[0], ", ".join(p[1])), sorted(self.__domain.items(), key=lambda p: p[0])))

    def print_domain(self):
        for letter, letter_domain in self.__domain.items():
            print("%s: %s" % (letter, ", ".join(letter_domain)))

    def __lt__(self, other):
        return True


def to_segment_and_digits(segment):
    return segment, numbers_domain(segment)


def segment_domain(digit):
    if digit == 0:
        return 'a', 'b', 'c', 'e', 'f', 'g'
    if digit == 1:
        return 'c', 'f'
    if digit == 2:
        return 'a', 'c', 'd', 'e', 'g'
    if digit == 3:
        return 'a', 'c', 'd', 'f', 'g'
    if digit == 4:
        return 'b', 'c', 'd', 'f'
    if digit == 5:
        return 'a', 'b', 'd', 'f', 'g'
    if digit == 6:
        return 'a', 'b', 'd', 'e', 'f', 'g'
    if digit == 7:
        return 'a', 'c', 'f'
    if digit == 8:
        return 'a', 'b', 'c', 'd', 'e', 'f', 'g'
    return 'a', 'b', 'c', 'd', 'f', 'g'


def reverse_digit(string):
    if string == 'abcefg':
        return 0
    if string == 'cf':
        return 1
    if string == 'acdeg':
        return 2
    if string == 'acdfg':
        return 3
    if string == 'bcdf':
        return 4
    if string == 'abdfg':
        return 5
    if string == 'abdefg':
        return 6
    if string == 'acf':
        return 7
    if string == 'abcdefg':
        return 8
    return 9


def all_segments_domain(segment, digit):
    domain = segment_domain(digit)

    return {c: domain for c in segment}


def numbers_domain(segments):
    """
    digit: segments
    1: 2
    7: 3
    4: 4
    8: 7

    2: 5
    3: 5
    5: 5

    0: 6
    6: 6
    9: 6

    :return map[letter, letter_domain]
    """

    if len(segments) == 2:
        return 1,
    elif len(segments) == 3:
        return 7,
    elif len(segments) == 4:
        return 4,
    elif len(segments) == 7:
        return 8,
    elif len(segments) == 5:
        return 2, 3, 5
    else:
        return 0, 6, 9


def search_domain(starting_domain):
    starting_domain.run_domain()
    frontier = [(0, starting_domain)]
    visited = set()

    while len(frontier) > 0:
        answer = step(frontier, visited)
        if answer:
            return answer


def step(frontier, visited):
    steps, domain = heappop(frontier)

    domain.run_domain()

    string = domain.to_string()
    if string in visited:
        return None

    visited.add(string)

    if domain.is_goal():
        return domain

    if domain.is_valid():
        for action in domain.digit_actions():
            heappush(frontier, (steps - 1, action))


def decode_all(segments):
    main_digs, sign_digs = segments.split(" | ")
    main_digs = main_digs.split(" ")
    sign_digs = sign_digs.split(" ")

    main_digs_domain = list(map(to_segment_and_digits, main_digs))
    sign_digs_domain = list(map(to_segment_and_digits, sign_digs))

    domain = Domain(main_digs_domain, sign_digs_domain)

    answer = search_domain(domain)

    count = 0
    for i, segments in enumerate(sign_digs):
        decoded = reverse_digit(answer.map(segments))
        count += decoded * pow(10, (3 - i))

    return count


def decode_several(lines):
    total_count = 0
    for line in lines:
        total_count += decode_all(line.strip())
    return total_count


def run():
    return decode_several(from_file("inputs/08_displays"))


def main():
    test(61229, decode_several(from_file("test_inputs/08_displays")))
    test(1027422, run())


if __name__ == '__main__':
    main()
