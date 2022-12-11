from Util import from_file, test


class Monkey:
    def __init__(self, name, s_items, operation, test, if_true, if_false):
        self.__name = name
        self.__items = s_items
        self.__operation = operation
        self.__test = test
        self.__if_true = if_true
        self.__if_false = if_false

        self.__inspected = 0

    def __str__(self):
        return "Monkey %d" % self.__name

    def __update_worry_level(self, old):
        return eval(self.__operation)

    def _throw_item(self, item, extreme_worry, name_to_monkey, reduce):
        updated_level = self.__update_worry_level(item)

        if extreme_worry:
            updated_level = updated_level % reduce
        else:
            updated_level = int(updated_level / 3)

        if updated_level % self.__test == 0:
            to_throw = self.__if_true
        else:
            to_throw = self.__if_false

        monkey = name_to_monkey[to_throw]
        monkey.receive_item(updated_level)

    def take_turn(self, extreme_worry, name_to_monkey, divisors):
        while len(self.__items) > 0:
            self.__inspected += 1
            item = self.__items.pop(0)
            self._throw_item(item, extreme_worry, name_to_monkey, divisors)

    def receive_item(self, item):
        self.__items.append(item)

    def get_name(self):
        return self.__name

    def get_inspected(self):
        return self.__inspected

    def get_test(self):
        return self.__test

    def print_items(self):
        print("Monkey %d: %s" % (self.__name, ", ".join(map(str, self.__items))))

    def get_items(self):
        return self.__items


def parse_monkey(lines):
    name = int(lines.pop(0).strip().split(" ")[1][:-1])

    starting = lines.pop(0).strip()
    s_items = list(map(lambda x: int(x), starting.split(": ")[1].split(", ")))

    operation = lines.pop(0).strip().split(": ")[1].split(" = ")[1]

    test = int(lines.pop(0).strip().split("divisible by ")[1])

    if_true = int(lines.pop(0).strip().split("throw to monkey ")[1])
    if_false = int(lines.pop(0).strip().split("throw to monkey ")[1])

    return Monkey(name, s_items, operation, test, if_true, if_false)


def parse_input(lines):
    monkeys = []
    name_to_monkey = {}

    divisors = 1

    while len(lines) > 0:
        monkey = parse_monkey(lines)
        monkeys.append(monkey)
        name_to_monkey[monkey.get_name()] = monkey

        divisors *= monkey.get_test()

        lines.pop(0)

    return monkeys, name_to_monkey, divisors


def simulate_game(lines, rounds, extreme_worry):
    monkeys, name_to_monkey, divisors = parse_input(lines)

    for i in range(rounds):
        for monkey in monkeys:
            monkey.take_turn(extreme_worry, name_to_monkey, divisors)

    inspected = sorted(list(map(lambda m: m.get_inspected(), monkeys)))
    return inspected[-1] * inspected[-2]


def run():
    return simulate_game(from_file("inputs/11_monkeys"), 10000, True)


def main():
    test(10605, simulate_game(from_file("test_inputs/11_monkeys"), 20, False))
    test(90882, simulate_game(from_file("inputs/11_monkeys"), 20, False))

    test(2713310158, simulate_game(from_file("test_inputs/11_monkeys"), 10000, True))
    print(run())


if __name__ == '__main__':
    main()

