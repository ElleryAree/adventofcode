from Util import test, from_file


def is_valid(opening, closing):
    if closing == ')' and opening != '(':
        return False

    if closing == '}' and opening != '{':
        return False

    if closing == '>' and opening != '<':
        return False

    if closing == ']' and opening != '[':
        return False

    return True


def get_score(c):
    if c == ')':
        return 3
    if c == ']':
        return 57
    if c == '}':
        return 1197
    if c == '>':
        return 25137
    return 0


def find_valid(line):
    queue = []

    for c in line:
        if c in ('{', '[', '(', '<'):
            queue.append(c)
        else:
            opening = queue.pop()
            if not is_valid(opening, c):
                return get_score(c), None

    return 0, queue


def completion_score(c):
    if c == '(':
        return 1
    if c == '[':
        return 2
    if c == '{':
        return 3
    if c == '<':
        return 4
    return 0


def complete(rest):
    count = 0
    while len(rest) > 0:
        count = count * 5 + completion_score(rest.pop())
    return count


def for_all(lines):
    count = 0

    for line in lines:
        score, _ = find_valid(line.strip())
        count += score

    return count


def for_all_complete(lines):
    counts = []

    for line in lines:
        score, rest = find_valid(line.strip())
        if score == 0:
            counts.append(complete(rest))

    sorted_count = list(sorted(counts))

    return sorted_count[int(len(sorted_count) / 2)]


def run():
    return for_all_complete(from_file("inputs/10_code"))


def main():
    test(26397, for_all(from_file("test_inputs/10_code")))
    print(for_all(from_file("inputs/10_code")))

    test(288957, for_all_complete(from_file("test_inputs/10_code")))
    print(run())


if __name__ == '__main__':
    main()
