from Util import test, from_file


def break_line(line, colored_bags):
    bag_color_start = line.find(" bags contain")
    bag_color = line[:bag_color_start]

    if bag_color in colored_bags:
        bag = colored_bags[bag_color]
    else:
        bag = Bag(bag_color)
        colored_bags[bag_color] = bag

    contains = line[len(bag_color) + len(" bags contain "):]

    if contains == "no other bags.":
        return

    for contained in contains.split(", "):
        amount_index = contained.find(" ")
        color_index = contained.rfind(" ")

        amount = int(contained[:amount_index])
        color = contained[amount_index + 1:color_index]

        if color in colored_bags:
            contained_bag = colored_bags[color]
        else:
            contained_bag = Bag(color)
            colored_bags[color] = contained_bag

        bag.add_contains(amount, contained_bag)
        contained_bag.add_container(bag)


def parse_lines(lines, f):
    colored_bags = {}

    for line in lines:
        line = line.strip()
        break_line(line, colored_bags)

    return f(colored_bags)


def find_gold_bags(colored_bags):
    possible_bags = set()

    queue = [colored_bags["shiny gold"]]

    while len(queue) > 0:
        bag = queue.pop()

        for a_bag in bag.can_be_contained:
            possible_bags.add(a_bag.color)
            queue.append(a_bag)

    return len(possible_bags)


def from_gold_bags(colored_bags):
    return colored_bags["shiny gold"].get_bags() - 1


class Bag:
    def __init__(self, color):
        self.color = color
        self.__can_contain = []
        self.can_be_contained = []
        self.__bags_count = -1

    def add_contains(self, amount, bag):
        self.__can_contain.append((amount, bag))

    def add_container(self, bag):
        self.can_be_contained.append(bag)

    def get_bags(self):
        if self.__bags_count > 0:
            return self.__bags_count

        self.__bags_count = 1

        for amount, bag in self.__can_contain:
            self.__bags_count += amount * bag.get_bags()

        return self.__bags_count

    def __str__(self):
        return self.color


def run():
    return parse_lines(from_file("inputs/07_color_codes"), from_gold_bags)


if __name__ == '__main__':
    input = ["light red bags contain 1 bright white bag, 2 muted yellow bags.",
             "dark orange bags contain 3 bright white bags, 4 muted yellow bags.",
             "bright white bags contain 1 shiny gold bag.",
             "muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.",
             "shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.",
             "dark olive bags contain 3 faded blue bags, 4 dotted black bags.",
             "vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.",
             "faded blue bags contain no other bags.",
             "dotted black bags contain no other bags."]

    input_other_direction = ["shiny gold bags contain 2 dark red bags.\n",
                             "dark red bags contain 2 dark orange bags.\n",
                             "dark orange bags contain 2 dark yellow bags.\n",
                             "dark yellow bags contain 2 dark green bags.\n",
                             "dark green bags contain 2 dark blue bags.\n",
                             "dark blue bags contain 2 dark violet bags.\n",
                             "dark violet bags contain no other bags.\n", ]

    test(4, parse_lines(input, find_gold_bags))
    test(296, parse_lines(from_file("inputs/07_color_codes"), find_gold_bags))

    test(32, parse_lines(input, from_gold_bags))
    test(126, parse_lines(input_other_direction, from_gold_bags))

    print(run())
