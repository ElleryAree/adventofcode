from collections import deque

from Util import test, from_file


def execute(left, operation, right):
    left = int(left)
    right = int(right)

    if operation == '+':
        return left + right
    if operation == '*':
        return left * right


def calc(queue):
    while len(queue) > 1:
        left = queue.popleft()
        operation = queue.popleft()
        right = queue.popleft()

        while '(' in right:
            ind = right.rfind('(')
            rem = right[:ind]
            queue.appendleft(right[ind + 1:])

            right = "%s%s" % (rem, calc(queue))

        if ')' in right:
            ind = right.find(')')
            rem = right[ind + 1:]

            return "%d%s" % (execute(left, operation, right[:ind]), rem)

        res = execute(left, operation, right)
        queue.appendleft(res)

    return queue.pop()


def set_parens(queue) -> deque:
    new_queue = deque()

    while len(queue) > 1:
        left = queue.popleft()
        operation = queue.popleft()
        right = queue.popleft()

        if operation == '*':
            new_queue.append(left)
            new_queue.append(operation)

            queue.appendleft(right)
            continue

        new_queue.append("(" + left)

        while operation == '+':
            new_queue.append(operation)
            new_queue.append(right)
            left = right

            if len(queue) < 2:
                break

            operation = queue.popleft()
            right = queue.popleft()

        new_queue.pop()
        new_queue.append(left + ")")
        new_queue.append(operation)

        queue.appendleft(right)

    new_queue.pop()

    return new_queue


def calc_exp(expression):
    expression.append('+')
    expression.append('0')
    with_parens = set_parens(expression)
    with_parens.appendleft('+')
    with_parens.appendleft('0')
    return calc(with_parens)


def compute_parens(line):
    queue = deque()

    for i, c in enumerate(line):
        if c != ')':
            queue.append(c)
            continue

        expression = deque()

        exp_c = queue.pop()
        while exp_c != '(':
            expression.appendleft(exp_c)
            exp_c = queue.pop()

        value = calc_exp(expression)

        queue.append(str(value))

    return calc_exp(queue)


def set_parens_2(queue, start) -> str:
    state = start
    while len(queue) > 0:
        next_s = queue.popleft()

        state = state.next_state(next_s)

    return str(state)


def parse_line(line):
    queue = deque()
    queue.extend(line.strip().split(" "))

    return queue


def parse_with_parenthesis(line) -> int:
    line = line.strip().replace(" ", "")

    return int(compute_parens(line))


def run_lines(lines, parser):
    total = 0

    for line in lines:
        total += parser(line)
    return total


def run():
    return run_lines(from_file("inputs/18_homework"), parse_with_parenthesis)


if __name__ == '__main__':
    test(6, parse_with_parenthesis("1 * 2 * 3"))
    test(6, parse_with_parenthesis("1 + 2 + 3"))
    #
    test(55, parse_with_parenthesis("1 + ((4 + 5) * 6)"))
    test(35, parse_with_parenthesis("1 + (4 + (5 * 6))"))
    test(6, parse_with_parenthesis("1 + (2 + 3)"))
    test(7, parse_with_parenthesis("1 + (2 * 3)"))
    #
    test(51, parse_with_parenthesis("1 + (2 * 3) + (4 * (5 + 6))"))
    test(46, parse_with_parenthesis("2 * 3 + (4 * 5)"))
    test(1445, parse_with_parenthesis("5 + (8 * 3 + 9 + 3 * 4 * 3)"))
    test(669060, parse_with_parenthesis("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"))
    test(23340, parse_with_parenthesis("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"))

    print(run())

    # test(231, calc(parse_with_parenthesis("1 + 2 * 3 + 4 * 5 + 6")))
    # test(231, calc(parse_with_parenthesis("1 + (2 * 3) + (4 * (5 + 6))")))
    #
    # test(71, calc(parse_line("1 + 2 * 3 + 4 * 5 + 6")))
    # test(51, calc(parse_line("1 + (2 * 3) + (4 * (5 + 6))")))
    # test(26, calc(parse_line("2 * 3 + (4 * 5)")))
    # test(437, calc(parse_line("5 + (8 * 3 + 9 + 3 * 4 * 3)")))
    # test(12240, calc(parse_line("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))")))
    # test(13632, calc(parse_line("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2")))
    #
    # test(23507031841020, run_lines(from_file("inputs/18_homework"), parse_line))
