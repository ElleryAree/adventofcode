from Util import test, from_file


class Condition:
    def __init__(self, register, condition, value):
        self.__register = register
        self.__condition = condition
        self.__value = value

    def is_true(self, registers):
        register = registers.get(self.__register, 0)

        if self.__condition == '>':
            return register > self.__value
        if self.__condition == '>=':
            return register >= self.__value
        if self.__condition == '<':
            return register < self.__value
        if self.__condition == '<=':
            return register <= self.__value
        if self.__condition == '==':
            return register == self.__value
        if self.__condition == '!=':
            return register != self.__value
        return False

    def __str__(self):
        return "if %s %s %s" % (self.__register, self.__condition, self.__value)


class Operation:
    def __init__(self, register, op, amount, condition):
        self.__register = register
        self.__op = op
        self.__amount = amount
        self.__condition = condition

    def update(self, registers):
        register = registers.get(self.__register, 0)

        if not self.__condition.is_true(registers):
            return register

        if self.__op == 'inc':
            register += self.__amount
        else:
            register -= self.__amount

        registers[self.__register] = register

        return register

    def __str__(self):
        return "%s %s %s %s" % (self.__register, self.__op, self.__amount, self.__condition)


def parse_line(line):
    parts = line.strip().split(" if ")

    left_parts = parts[0].split()
    up_register = left_parts[0]
    up_op = left_parts[1]
    up_amount = int(left_parts[2])

    right_parts = parts[1].split()
    c_register = right_parts[0]
    c_op = right_parts[1]
    c_amount = int(right_parts[2])

    condition = Condition(c_register, c_op, c_amount)
    return Operation(up_register, up_op, up_amount, condition)


def parse_lines(lines):
    return list(map(parse_line, lines))


def find_max(lines):
    operations = parse_lines(lines)
    registers = {}

    max_updated = 0

    for operation in operations:
        updated_value = operation.update(registers)
        if updated_value > max_updated:
            max_updated = updated_value

    return max(registers.values()), max_updated


def main():
    test_part_1, test_part_2 = find_max(from_file("test_inputs/08_registers"))
    part_1, part_2 = find_max(from_file("inputs/08_registers"))

    test(1, test_part_1)
    test(5966, part_1)

    test(10, test_part_2)
    print(part_2)


if __name__ == '__main__':
    main()
