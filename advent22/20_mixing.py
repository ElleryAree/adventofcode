from copy import copy, deepcopy

from Util import from_file, test


class Node:
    def __init__(self, value, i):
        self.value = value
        self.i = i
        self.prev_node = None
        self.next_node = None


class LinkedList:
    def __init__(self):
        self.head = Node(None, -1)
        self.tail = self.head

        self.node_map = {}
        self.size = 0

        self.head.next_node = self.tail
        self.head.prev_node = self.tail

        self.tail.next_node = self.head
        self.tail.prev_node = self.head

    @staticmethod
    def __insert_between(prev_node, node, next_node):
        prev_node.next_node = node
        node.prev_node = prev_node

        next_node.prev_node = node
        node.next_node = next_node

    def add_at_end(self, value):
        next_node = Node(value, self.size)
        self.node_map[next_node.i] = next_node
        self.__insert_between(self.tail.prev_node, next_node, self.tail)
        self.size += 1

    def as_list(self):
        node = self.head.next_node
        arr = []

        for i in range(self.size):
            arr.append(node.value)
            node = node.next_node

        return arr


def parse_input(lines):
    llist = LinkedList()

    for line in lines:
        llist.add_at_end(int(line.strip()))

    return llist


def parse_input_to_list(mult, lines):
    numbers = []
    i_to_num = {}
    num_to_i = {}

    numbers_set = set()
    start = None

    for i, line in enumerate(lines):
        # value = int(line.strip()) * mult
        value = int(line.strip())

        if value == 0:
            start = i, value

        value = i, value

        i_to_num[len(numbers)] = value
        num_to_i[value] = len(numbers)
        numbers.append(value)
        numbers_set.add(value)

    if len(numbers) != len(numbers_set):
        print("there are duplicates")
        return None

    return numbers, i_to_num, num_to_i, start


def mix_list(llist):
    node = llist.head.next_node
    size = llist.size

    for _ in range(size):
        value = node.value

        # node_at_index =

        # prev_node =

    return llist


def move_number(i_to_num, num_to_i, number, numbers):
    if number[1] == 0:
        return

    i = num_to_i[number]
    index = i + number[1]

    if index < 0:
        print("Less then:")
        print("   Fast strategy: %d" % (index % len(numbers) + 1))

        next_index = index
        while next_index <= 0:
            next_index = len(numbers) - 1 + next_index
            # index = index % len(numbers) + 1
            # index = -index
            # while index >= len(numbers):
            #     index -= len(numbers)
            # index = -index
        print("Working strategy: %d" % next_index)
        print()
        index = next_index

    if index >= len(numbers):
        index = index % len(numbers) + 1
        # print("More then:")
        # print("   Fast strategy: %d" % (index % len(numbers) + 1))
        # while index >= len(numbers):
        #     index -= len(numbers) - 1
        #     # index = index % len(numbers) + 1
        # print("Working strategy: %d" % index)
        # print()


    ###########################################
    # DEBUG ###################################
    ###########################################
    # index_after = (index + 1)  % len(numbers)
    #
    # insert_after = i_to_num[index]
    # insert_before = i_to_num[index_after]
    ###########################################

    if i < index:
        for to_move in range(i + 1, index + 1):
            num_to_move = i_to_num[to_move]
            num_to_i[num_to_move] -= 1

            # if num_to_i[num_to_move] < 0:
            #     num_to_i[num_to_move] = len(numbers) - 1

            i_to_num[to_move - 1] = i_to_num[to_move]

        num_to_i[number] = index
        i_to_num[index] = number
    else:
        for to_move in range(i - 1, index - 1, -1):
            num_to_move = i_to_num[to_move]

            num_to_i[num_to_move] += 1
            # if num_to_i[num_to_move] >= len(numbers):
            #     num_to_i[num_to_move] = 0

            i_to_num[to_move + 1] = i_to_num[to_move]

        num_to_i[number] = index
        i_to_num[index] = number

    ###########################################
    # DEBUG ###################################
    ###########################################
    # print("%d moves between %d and %d" % (number[1], insert_after[1], insert_before[1]))
    #
    # test_list_1 = []
    # for other_i in sorted(i_to_num):
    #     test_list_1.append("%s" % i_to_num[other_i][1])
    #     # test_list_1.append(i_to_num[other_i][1])
    #
    # print("Actual list: %s" % ", ".join(map(str, test_list_1)))
    # print(test_list_1)
    # print()
    ###########################################


def mix_numbers(times, data):
    numbers, i_to_num, num_to_i, start = data
    orig_number = deepcopy(numbers)

    # test_list_1 = []
    # for other_i in sorted(i_to_num):
    #     test_list_1.append("%s" % i_to_num[other_i][1])
    #
    # print(" Start list: %s" % ", ".join(test_list_1))

    for _ in range(times):
        for number in orig_number:
            move_number(i_to_num, num_to_i, number, numbers)

    test_list_1 = []
    for other_i in sorted(i_to_num):
        test_list_1.append(i_to_num[other_i][1])

    return test_list_1, num_to_i, start


def find_at(indices, data):
    numbers, num_to_i, start = data
    total = 0

    # for index in indices:
    #     scaled = index % len(numbers)
    #     print("On step %d i is %d" % (index, scaled))
        # value = numbers[scaled]
        # total += value

    # print("Starting list is: %s" % numbers)

    i = num_to_i[start]
    for c in range(indices[-1] + 1):
        if c in indices:
            # print("On step %d i is %d value is %d" % (c, i, numbers[i]))
            total += numbers[i] * 811589153

        i += 1
        if i >= len(numbers):
            i = 0

    return total


def find_at_brut(indices, llist):
    total = 0
    node = llist.head.next_node

    for i in range(indices[-1] + 1):
        if i in indices:
            total += node.value
        node = node.next_node

    return total


def as_llist(arr):
    llist = LinkedList()
    for i in arr:
        llist.add_at_end(i)
    return llist


def as_numbs(arr):
    numbers = []
    i_to_num = {}
    num_to_i = {}
    start = (0, 0)

    for i, v in enumerate(arr):
        if v == 0:
            start = i, v

        v = i, v
        i_to_num[i] = v
        num_to_i[v] = i
        numbers.append(v)

    return numbers, i_to_num, num_to_i, start


def test_mix(starting_list, expected_list, number, before, after):
    numbers, i_to_num, num_to_i, _ = as_numbs(starting_list)

    print("Expected:")
    print("%d moves between %d and %d:" % (number[1], before, after))
    print(" Start list: %s" % ", ".join(map(str, starting_list)))
    print("Target list: %s" % ", ".join(map(str, expected_list)))
    print()
    print("Actual:")
    move_number(i_to_num, num_to_i, number, numbers)


def main():
    # test(3, find_at_brut([1000, 2000, 3000], as_llist([1, 2, -3, 4, 0, 3, -2])))

    print(mix_numbers(1, as_numbs([8, 2, 32, -41, 6, 29, -4, 6, -8, 8, -3, -8, 3, -5, 0, -1, 2, 1, 10, -9]))[0])

    # test(3, find_at([1000, 2000, 3000], mix_numbers(1, parse_input_to_list(1, from_file("test_inputs/20_mixing")))))
    # test(17490, find_at([1000, 2000, 3000], mix_numbers(1, parse_input_to_list(1, from_file("inputs/20_mixing")))))

    # test(1623178306, find_at([1000, 2000, 3000], mix_numbers(1, parse_input_to_list(811589153, from_file("test_inputs/20_mixing")))))
    # print(find_at([1000, 2000, 3000], mix_numbers(10, parse_input_to_list(811589153, from_file("inputs/20_mixing")))))


    # test_mix([1, 2, -3, 3, -2, 0, 4], [2, 1, -3, 3, -2, 0, 4], (0, 1), 2, -3)
    # test_mix([2, 1, -3, 3, -2, 0, 4], [1, -3, 2, 3, -2, 0, 4], (0, 2), -3, 3)
    # test_mix([1, 2, 3, -2, -3, 0, 4], [1, 2, -2, -3, 0, 3, 4], (2, 3), 0, 4)
    # test_mix([1, -3, 2, 3, -2, 0, 4], [1, 2, 3, -2, -3, 0, 4], (1, -3), -2, 0)
    # test_mix([1, 2, -2, -3, 0, 3, 4], [1, 2, -3, 0, 3, 4, -2], (2, -2), 4, 1)
    # test_mix([1, 2, -3, 0, 3, 4, -2], [1, 2, -3, 4, 0, 3, -2], (5, 4), -3, 0)

    # test_mix([1, 2, -3, 0, 3, -10, -2], [1, 2, -3, -10, 0, 3, -2], -10, -3, 0)
    # test_mix([1, 2, -3, 0, 3, -23, -2], [1, 2, -3, 0, -23, 3, -2], -23, -3, 0)

    # test_mix([8, 2, 32, -41, 6, 29, -4, 6, -8, 8, -3, -8, 3, -5, 0, -1, 2, 1, 10, -9],
    #          [2, 32, -41, 6, 29, -4, 6, -8, 8, 8, -3, -8, 3, -5, 0, -1, 2, 1, 10, -9], (0, 8), -8, 8)
    #
    # test_mix([2, 32, -41, 6, 29, -4, 6, -8, 8, 8, -3, -8, 3, -5, 0, -1, 2, 1, 10, -9],
    #          [32, -41, 2, 6, 29, -4, 6, -8, 8, 8, -3, -8, 3, -5, 0, -1, 2, 1, 10, -9], (0, 2), -41, 6)

    # test_mix([32, -41, 2, 6, 29, -4, 6, -8, 8, 8, -3, -8, 3, -5, 0, -1, 2, 1, 10, -9],
    #          [-41, 2, 6, 29, -4, 6, -8, 8, 8, -3, -8, 3, -5, 32, 0, -1, 2, 1, 10, -9], (0, 32), -5, -0)

    # test_mix([-41, 2, 6, 29, -4, 6, -8, 8, 8, -3, -8, 3, -5, 32, 0, -1, 2, 1, 10, -9],
    #          [2, 6, 29, -4, 6, -8, 8, 8, -3, -8, 3, -5, 32, 0, -1, 2, -41, 1, 10, -9], (0, -41), 2, 1)

    # [2, 8, 6, 6, 29, 32, 3, 8, 0, -8, -1, 2, -41, -8, -4, 1, 10, -9, -5, -3]
    # [2, 8, 6, 6, 29, 32, 3, 8, 0, -1, -8, 2, -41, -8, -4, 1, 10, -9, -5, -3]

    # test_mix([2, 8, 6, 6, 29, 32, 3, 8, 0, -8, -1, 2, -41, -8, -4, 1, 10, -9, -5, -3],
    #          [2, 8, 6, 6, 29, 32, 3, 8, 0, -1, -8, 2, -41, -8, -4, 1, 10, -9, -5, -3], (10, -1), 2, 1)

    # test_mix([0, -8, -1, 2],
    #          [0, -1, -8, 2], (2, -1), 2, 1)

"""
[2, 8, 6, 6, 29, 32, 10, 3, -9, 8, 0, -1, -8, -41, -8, 2, -4, 1, -5, -3]
[2, 8, 6, 6, 29, 32, 10, 3, -9, 8, 0, -1, -8, -41, -8, 2, -4, 1, -5, -3]

"""


if __name__ == '__main__':
    main()
