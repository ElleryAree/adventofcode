from Util import test, from_file


class Program:
    def __init__(self, name):
        self.name = name
        self.weight = -1
        self.disc_weight = 0

        self.parent = None
        self.children = []

        self.expected_weight = 0

    @staticmethod
    def __find_diff(weights):
        most = 0
        underdog = 0
        for weight, subs in weights.items():
            if len(subs) == 1:
                underdog = subs[0]
            else:
                most = weight

        underdog_disc = underdog.disc_weight
        expected_weight = most - underdog_disc

        return expected_weight


    def update_weight(self, tower):
        weights = {}

        for sub in self.children:
            sub_program = tower[sub]

            update = sub_program.update_weight(tower)
            sub_weight, diff = update

            if sub_weight is None:
                return update

            self.disc_weight += sub_weight

            weight_count = weights.get(sub_weight)
            if weight_count is None:
                weight_count = []
                weights[sub_weight] = weight_count
            weight_count.append(sub_program)

        if len(weights) > 1 and len(self.children) > 1:
            return None, self.__find_diff(weights)

        return self.weight + self.disc_weight, None

    def __str__(self):
        return self.name


def parse_line(line):
    parts = line.strip().split(" -> ")

    name, weight = parts[0].split(" ")
    weight = weight[1:-1]
    subs = [] if len(parts) < 2 else parts[1].split(", ")

    return name, weight, subs


def get_or_create(name, tower):
    program = tower.get(name)
    if program is None:
        program = Program(name)
        tower[name] = program
    return program


def parse(lines):
    tower = {}

    program = None

    for line in lines:
        name, weight, subs = parse_line(line)

        program = get_or_create(name, tower)
        program.weight = int(weight)
        program.children = subs

        for sub in subs:
            sub_program = get_or_create(sub, tower)
            sub_program.parent = program

    parent = program.parent
    while parent is not None:
        program = parent
        parent = program.parent

    _, answer = program.update_weight(tower)

    return program.name, answer


def main():
    test_part_1, test_part_2 = parse(from_file("test_inputs/07_towers"))
    part_1, part_2 = parse(from_file("inputs/07_towers"))

    test("tknk", test_part_1)
    test("bpvhwhh", part_1)

    test(60, test_part_2)
    print(part_2)


if __name__ == '__main__':
    main()
