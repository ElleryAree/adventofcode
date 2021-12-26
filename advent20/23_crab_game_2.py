from Util import test


class Node:
    def __init__(self, value):
        self.prev = None
        self.next = None
        self.value = value

    def __str__(self):
        return str(self.value)


def insert(node, before, after):
    before.next = node
    node.prev = before

    after.prev = node
    node.next = after


class LinkedList:
    def __init__(self):
        self.__indices = {}
        self.__head = None
        self.__tail = None

        self.min = 2000000
        self.max = -1

    def head(self):
        return self.__head

    def add(self, value):
        if value > self.max:
            self.max = value
        if value < self.min:
            self.min = value

        node = Node(value)
        self.__indices[value] = node

        if self.__tail is None:
            self.__tail = node
            self.__head = node
        else:
            insert(node, self.__tail, self.__head)
            self.__tail = node

        return node

    def str_list(self, start=None):
        str_rep = ""
        start = self.__head if start is None else start
        node = start.next

        while node != start:
            str_rep += str(node.value)
            node = node.next

        return str_rep

    def find(self, target):
        return self.__indices[target]


def game(cups, max_turns):
    selected = cups.head()
    for i in range(max_turns):
        first_cup = selected.next
        second_cup = first_cup.next
        third_cup = second_cup.next

        destination_value = selected.value - 1
        if destination_value < cups.min:
            destination_value = cups.max

        while destination_value == first_cup.value or destination_value == second_cup.value or destination_value == third_cup.value:
            destination_value = destination_value - 1

            if destination_value < cups.min:
                destination_value = cups.max

        destination = cups.find(destination_value)

        # remove selection
        before_first = first_cup.prev
        after_next = third_cup.next

        before_first.next = after_next
        after_next.prev = before_first

        # insert selection back
        after_dest = destination.next
        destination.next = first_cup
        first_cup.prev = destination

        third_cup.next = after_dest
        after_dest.prev = third_cup

        # select next
        selected = selected.next

    return cups


def run_one(line, max_turns):
    cups = make_linked_list(line)
    cups = game(cups, max_turns)
    return cups.str_list(start=cups.find(1))


def run_many(line):
    cups = make_linked_list(line)
    max_num = cups.max
    target_size = 1000000 - len(line)

    for i in range(target_size):
        number = max_num + i + 1
        cups.add(number)

    cups = game(cups, 10000000)
    number_one = cups.find(1)

    part_1 = number_one.next
    part_2 = part_1.next

    # print("Part 1: %s, part 2: %s" % (part_1, part_2))

    return part_1.value * part_2.value


def make_linked_list(line):
    llist = LinkedList()

    for c in line:
        c = int(c)
        llist.add(c)

    return llist


def run():
    return run_many("952316487")


if __name__ == '__main__':
    test("92658374", run_one("389125467", 10))
    test("67384529", run_one("389125467", 100))
    test("25398647", run_one("952316487", 100))

    test(149245887792, run_many("389125467"))
    print(run())
