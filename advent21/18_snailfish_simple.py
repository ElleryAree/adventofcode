from __future__ import annotations

import string
from heapq import heappush, heappop
from math import ceil, floor
from Util import test, from_file


def parse_string(line):
    return eval(line)


def test_parse(line):
    test(line, str(parse_string(line)))


def combine_lines(lines):
    first = parse_string(lines[0].strip())

    for i in range(1, len(lines)):
        first = do_run(first)
        second = parse_and_run(lines[i].strip())

        first = [first, second]

    return first


def magnitude(start):
    acc = 0
    for i, item in enumerate(start):
        if isinstance(item, int):
            value = item
        else:
            value = magnitude(item)

        if i == 0:
            acc += 3 * value
        else:
            acc += 2 * value

    return acc


def explode(start, global_i, target_i, pair):
    for i, item in enumerate(start):
        if isinstance(item, int):
            if global_i == target_i - 1:
                start[i] += pair[0]
            if global_i == target_i + 1:
                start[i] += pair[1]
                return global_i, True

            global_i += 1
        else:
            next_global_i, was_found = explode(item, global_i, target_i, pair)
            if was_found:
                return next_global_i, was_found

            global_i = next_global_i
    return global_i, False


def find_reduce(start, level, global_i, include_split):
    if level >= 4:
        return global_i, ("explode", start)

    for i, item in enumerate(start):
        if isinstance(item, int):
            if item >= 10 and include_split:
                half = item / 2
                start[i] = [floor(half), ceil(half)]

                return global_i, ("split", item)

            global_i += 1
        else:
            next_global_i, action = find_reduce(item, level + 1, global_i, include_split)
            if action is not None:
                if action[0] == 'explode' and level == 3:
                    start[i] = 0

                return next_global_i, action

            global_i = next_global_i

    return global_i, None


def parse_and_run(line):
    start_node = parse_string(line)

    return do_run(start_node)


def do_run(start_node):
    target_i, action = find_reduce(start_node, 0, 0, False)
    if action is None:
        target_i, action = find_reduce(start_node, 0, 0, True)

    i = 0
    while action is not None:
        i += 1

        if action[0] == 'explode':
            explode(start_node, 0, target_i, action[1])

        target_i, action = find_reduce(start_node, 0, 0, False)
        if action is None:
            target_i, action = find_reduce(start_node, 0, 0, True)

    return start_node


def find_max(lines):
    max_mag = 0

    for i, first_line in enumerate(lines):
        for j, second_line in enumerate(lines):
            if i == j:
                continue

            mag = magnitude(do_run([parse_string(first_line), parse_string(second_line)]))
            if mag > max_mag:
                max_mag = mag

    return max_mag


def combine_and_run(lines):
    return do_run(combine_lines(lines))


def test_magnitude(expected, line):
    test(expected, magnitude(line))


def all_parse_tests():
    test_parse("[1, 2]")
    test_parse("[[1, 2], 3]")
    test_parse("[9, [8, 7]]")
    test_parse('[[1, 9], [8, 5]]')
    test_parse('[[[[1, 2], [3, 4]], [[5, 6], [7, 8]]], 9]')
    test_parse('[[[9, [3, 8]], [[0, 9], 6]], [[[3, 7], [4, 9]], 3]]')
    test_parse('[[[[1, 3], [5, 3]], [[1, 3], [8, 7]]], [[[4, 9], [6, 9]], [[8, 2], [7, 3]]]]')


def all_explode_tests():
    test([[[[0, 9], 2], 3], 4], parse_and_run('[[[[[9,8],1],2],3],4]'))
    test([7, [6, [5, [7, 0]]]], parse_and_run('[7,[6,[5,[4,[3,2]]]]]'))
    test([[6, [5, [7, 0]]], 3], parse_and_run('[[6,[5,[4,[3,2]]]],1]'))
    test([[3, [2, [8, 0]]], [9, [5, [7, 0]]]], parse_and_run('[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]'))
    test([[3, [2, [8, 0]]], [9, [5, [7, 0]]]], parse_and_run('[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]'))


def all_split_test():
    test([[[[5, 0], 8], 3], 4],  parse_and_run('[[[[[9, 8], 3], 2], 3], 4]'))


def all_magnitude_tests():
    test_magnitude(143, [[1, 2], [[3, 4], 5]])
    test_magnitude(1384, [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]])
    test_magnitude(445, [[[[1, 1], [2, 2]], [3, 3]], [4, 4]])
    test_magnitude(791, [[[[3, 0], [5, 3]], [4, 4]], [5, 5]])
    test_magnitude(1137, [[[[5, 0], [7, 4]], [5, 5]], [6, 6]])
    test_magnitude(3488, [[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]])


def test_all():
    combine_and_run(['[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]', '[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]'])


    # test([[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]],  parse_and_run('[[[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]]'))
    # test([[[[1, 1], [2, 2]], [3, 3]], [4, 4]],  combine_lines(['[1, 1]',  '[2, 2]',  '[3, 3]',  '[4, 4]']))

    # test([[[[3, 0], [5, 3]], [4, 4]], [5, 5]],  combine_and_run(["[1, 1]",  "[2, 2]",  "[3, 3]",  "[4, 4]",  "[5, 5]"]))
    # test([[[[5, 0], [7, 4]], [5, 5]], [6, 6]],  combine_and_run(['[1, 1]',  '[2, 2]',  '[3, 3]',  '[4, 4]',  '[5, 5]',  '[6, 6]']))

    # test([[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]],  combine_and_run(
    #     ['[[[0, [4, 5]], [0, 0]], [[[4, 5], [2, 6]], [9, 5]]]',  '[7, [[[3, 7], [4, 3]], [[6, 3], [8, 8]]]]']))

    # test([[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]],  combine_and_run(
    #     ['[[[0, [4, 5]], [0, 0]], [[[4, 5], [2, 6]], [9, 5]]]',  '[7, [[[3, 7], [4, 3]], [[6, 3], [8, 8]]]]',
    #      '[[2, [[0, 8], [3, 4]]], [[[6, 7], 1], [7, [1, 6]]]]',  '[[[[2, 4], 7], [6, [0, 5]]], [[[6, 8], [2, 8]], [[2, 1], [4, 5]]]]',
    #      '[7, [5, [[3, 8], [1, 4]]]]',  '[[2, [2, 2]], [8, [8, 1]]]',  '[2, 9]',  '[1, [[[9, 3], 9], [[9, 0], [0, 7]]]]',
    #      '[[[5, [7, 4]], 7], 1]',  '[[[[4, 2], 2], 6], [8, 7]]']))


def test_homework():
    test_input = from_file("test_inputs/18_snailfish")

    final = combine_and_run(test_input)
    test([[[[6, 6], [7, 6]], [[7, 7], [7, 0]]], [[[7, 7], [7, 7]], [[7, 8], [9, 9]]]], final)
    test(4140, magnitude(final))

    test(3993, find_max(test_input))


def run_homework():
    final = combine_and_run(from_file("inputs/18_snailfish"))
    test(3892, magnitude(final))

    test(4909, run())


def run():
    return find_max(from_file("inputs/18_snailfish"))


def main():
    # all_parse_tests()
    # all_explode_tests()
    # all_split_test()
    # all_magnitude_tests()
    test_all()

    # test_homework()
    # run_homework()


if __name__ == '__main__':
    main()
