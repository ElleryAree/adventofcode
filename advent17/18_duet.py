from Util import test, from_file


class Program:
    def __init__(self, p_id, instructions):
        self.queue = []
        self.send_times = 0

        self.__other_queue = []

        self.__instructions = instructions
        self.__registers = {'p': p_id}
        self.__instruction = 0

        self.__is_waiting_on = None

    def __execute_delayed(self, register):
        if len(self.__other_queue) < 1:
            self.__is_waiting_on = register
            return

        self.__registers[register] = self.__other_queue.pop(0)
        self.__is_waiting_on = None

    def __execute_normal(self):
        if self.__is_finished():
            return

        inc = 1
        parts = self.__instructions[self.__instruction]

        if parts[0] == "snd":
            self.send_times += 1
            self.queue.append(number_or_register(parts[1], self.__registers))
        if parts[0] == "set":
            self.__registers[parts[1]] = number_or_register(parts[2], self.__registers)
        if parts[0] == "add":
            self.__registers[parts[1]] = number_or_register(parts[1], self.__registers) + number_or_register(parts[2], self.__registers)
        if parts[0] == "mul":
            self.__registers[parts[1]] = number_or_register(parts[1], self.__registers) * number_or_register(parts[2], self.__registers)
        if parts[0] == "mod":
            self.__registers[parts[1]] = number_or_register(parts[1], self.__registers) % number_or_register(parts[2], self.__registers)
        if parts[0] == "rcv":
            self.__execute_delayed(parts[1])
        if parts[0] == "jgz" and number_or_register(parts[1], self.__registers) > 0:
            inc = number_or_register(parts[2], self.__registers)

        self.__instruction += inc

    def set_queue(self, queue):
        self.__other_queue = queue

    def execute(self):
        if self.__is_waiting():
            self.__execute_delayed(self.__is_waiting_on)
        else:
            self.__execute_normal()

    def __is_waiting(self):
        return self.__is_waiting_on is not None

    def __is_finished(self):
        return self.__instruction >= len(self.__instructions)

    def is_done(self):
        return self.__is_waiting() or self.__is_finished()



def number_or_register(value, registers):
    register = registers.get(value)
    return register if register is not None else int(value)


def execute(lines):
    lines = parse_lines(lines)

    registers = {}
    instruction = 0
    sound = 0

    while instruction < len(lines):
        inc = 1
        parts = lines[instruction]
        register = registers.get(parts[1], 0)

        if parts[0] == "snd":
            sound = register
        if parts[0] == "set":
            registers[parts[1]] = number_or_register(parts[2], registers)
        if parts[0] == "add":
            registers[parts[1]] = register + number_or_register(parts[2], registers)
        if parts[0] == "mul":
            registers[parts[1]] = register * number_or_register(parts[2], registers)
        if parts[0] == "mod":
            registers[parts[1]] = register % number_or_register(parts[2], registers)
        if parts[0] == "rcv" and register != 0:
            return sound
        if parts[0] == "jgz" and register > 0:
            inc = number_or_register(parts[2], registers)

        instruction += inc


def execute_part_2(lines):
    lines = parse_lines(lines)

    program_1 = Program(0, lines)
    program_2 = Program(1, lines)

    program_1.set_queue(program_2.queue)
    program_2.set_queue(program_1.queue)

    while not (program_1.is_done() and program_2.is_done()):
        program_1.execute()
        program_2.execute()

    return program_2.send_times


def parse_lines(lines):
    return list(map(lambda line: line.strip().split(" "), lines))


def main():
    test(4, execute(from_file("test_inputs/18_duet")))
    test(3423, execute(from_file("inputs/18_duet")))

    execute_part_2(["snd 1", "snd 2", "snd p", "rcv a", "rcv b", "rcv c", "rcv d"])
    print(execute_part_2(from_file("inputs/18_duet")))


if __name__ == '__main__':
    main()
