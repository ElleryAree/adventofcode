from Util import test, from_file


def parse_code(lines):
    code = []

    for line in lines:
        line = line.strip()

        op = line[:3]
        value = int(line[4:])
        code.append((op, value))

    return code


def run_one(lines):
    return Runtime().run(parse_code(lines))


def run_many(lines):
    code = parse_code(lines)

    for (i, (op, value)) in enumerate(code):
        if op == 'acc':
            continue

        switched_op = 'nop' if op == 'jmp' else 'jmp'
        code[i] = (switched_op, value)

        runtime = Runtime()
        acc = runtime.run(code)

        if not runtime.looped:
            return acc

        code[i] = (op, value)


class Runtime:
    def __init__(self):
        self.__acc = 0
        self.__current_line = 0
        self.looped = False

    def __acc_op(self, value):
        self.__acc += value
        return self.__current_line + 1

    def __jmp_op(self, value):
        return self.__current_line + value

    def run(self, code):
        visited = set()

        while self.__current_line < len(code):
            if self.__current_line in visited:
                self.looped = True
                break

            visited.add(self.__current_line)

            op, value = code[self.__current_line]

            if op == 'acc':
                next_line = self.__acc_op(value)
            elif op == 'jmp':
                next_line = self.__jmp_op(value)
            else:
                next_line = self.__current_line + 1

            self.__current_line = next_line

        return self.__acc


def run():
    return run_many(from_file("inputs/08_programm"))


if __name__ == '__main__':
    test_code = ["nop +0\n", "acc +1\n", "jmp +4\n", "acc +3\n", "jmp -3\n", "acc -99\n", "acc +1\n", "jmp -4\n", "acc +6\n"]
    test(5, run_one(test_code))
    test(1723, run_one(from_file("inputs/08_programm")))

    test(8, run_many(test_code))

    print(run())
