from __future__ import annotations

from typing import Union

from Util import from_file


class Var:
    def __init__(self, name):
        self.__name = name

    def __index(self):
        if self.__name == 'x':
            index = 1
        elif self.__name == 'y':
            index = 2
        elif self.__name == 'z':
            index = 3
        else:
            index = 0
        return index

    def get_value(self, memory: list[str]):
        return memory[self.__index()]

    def set_value(self, memory: list[str], value: str):
        memory[self.__index()] = value

    def __str__(self):
        return self.__name


class Number:
    def __init__(self, value):
        self.__value = value

    def get_value(self, memory: list[str]):
        return self.__value

    def __str__(self):
        return str(self.__value)


def execute(memory: list[str], name: str, a: Var, b: Union[Var, Number]):
    if name == 'inp':
        a.set_value(memory, 'input_n')
        return

    if name == 'add':
        value_a = a.get_value(memory)
        value_b = b.get_value(memory)

        if value_a == '0' and value_b == '0':
            a.set_value(memory, '0')
        elif value_a == '0':
            a.set_value(memory, value_b)
        elif value_b == '0':
            return
        else:
            a.set_value(memory, "(%s + %s)" % (value_a, value_b))
        return

    if name == 'mul':
        value_a = a.get_value(memory)
        value_b = b.get_value(memory)

        if value_a == '0' or value_b == '0':
            a.set_value(memory, '0')
        elif value_a == '1':
            a.set_value(memory, value_b)
        elif value_b == '1':
            return
        else:
            a.set_value(memory, "(%s * %s)" % (value_a, value_b))
        return

    if name == 'div':
        value_a = a.get_value(memory)
        value_b = b.get_value(memory)

        if value_a == '0':
            a.set_value(memory, '0')
        elif value_b == '1':
            return
        elif value_b == '0':
            return
        else:
            a.set_value(memory, "(floor(%s / %s) if (%s != 0) else %s )" % (value_a, value_b, value_b, value_a))

        return

    if name == 'mod':
        value_a = a.get_value(memory)
        value_b = b.get_value(memory)
        a.set_value(memory, "((%s %% %s) if (%s >= 0 and %s > 0) else %s )" % (value_a, value_b, value_a, value_b, value_a))
        return

    if name == 'eql':
        value_a = a.get_value(memory)
        value_b = b.get_value(memory)
        a.set_value(memory, "(1 if (%s == %s) else 0) " % (value_a, value_b))
        return


def parse_variable(raw_a):
    if raw_a in ('x', 'y', 'z', 'w'):
        return Var(raw_a)
    return Number(raw_a)


def parse_input(lines):
    program = []

    for line in lines:
        line = line.strip()

        if len(line) == 0:
            continue

        parts = line.split(' ')
        name = parts[0]
        a = parse_variable(parts[1])
        if len(parts) == 3:
            b = parse_variable(parts[2])
        else:
            b = None

        program.append((name, a, b))

    return program


def execute_cell(cell: str, value: int):
    cell = cell.replace("?", str(value))
    cell_value = eval(cell)
    return cell_value


def run_program(lines):
    program = parse_input(lines)

    memory = ['0', '0', '0', '0']
    finals = []
    count = 1

    for i, (name, a, b) in enumerate(program):
        if name == 'inp' and i > 0:
            func = "def z%d_f(z%d, input_n):\n\tfrom math import floor\n\treturn %s" % (count, count - 1, memory[-1])
            finals.append(func)

            memory = [
                run_eval(memory[0], "w%d" % count),
                run_eval(memory[1], "x%d" % count),
                run_eval(memory[2], "y%d" % count),
                run_eval(memory[3], "z%d" % count)
            ]

            count += 1

        execute(memory, name, a, b)

    func = "def z%d_f(z%d, input_n):\n\tfrom math import floor\n\treturn %s" % (count, count - 1, memory[-1])
    finals.append(func)

    return finals


def run_eval(cell, or_else):
    try:
        maybe_value = eval(cell)
        return maybe_value if isinstance(maybe_value, int) else or_else
    except:
        return or_else


def test_all(codes):
    for code in codes:
        exec(compile(code, '', 'exec'))

    funcs = ["z%d_f" % i for i in range(1, 15)]
    queue = [((0,), 0)]
    found = []

    for step in range(14):
        unique = {}
        not_unique = 0

        while len(queue) > 0:
            history, z = queue.pop()

            for n in range(9, 0, -1):
                f = funcs[step]
                value = eval("%s(%d, %d)" % (f, z, n))

                next_history = history + (n,)

                if value == 0 and step == 13:
                    found.append(int("".join(map(str, next_history))))

                if value in unique:
                    not_unique += 1
                    stored = unique[value]
                    if next_history > stored:
                        unique[value] = next_history

                    continue

                unique[value] = next_history

        for value, history in unique.items():
            queue.append((history, value))

    return max(found)


def run(lines):
    codes = run_program(lines)
    return test_all(codes)


def main():
    print(run(from_file("inputs/24_logic_unit")))


if __name__ == '__main__':
    main()

