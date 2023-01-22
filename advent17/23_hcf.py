from Util import from_file, test


class Program:
    def __init__(self, state):
        self.A = state
        self.B = 0
        self.C = 0
        self.D = 0
        self.E = 0
        self.F = 0
        self.G = 0
        self.H = 0

    def __do_stuff(self):
        self.G = self.D * self.E - self.B  # 11

        if self.G != 0:  # 14
            self.F = 0

        self.E += 1
        self.G = self.E - self.B  # 18

    def __do_more_stuff(self):
        self.E = 2  # 10

        self.__do_stuff()
        while self.G != 0:  # 19
            self.__do_stuff()

        self.D += 1

        self.G = self.D - self.B  # 22

    def run(self):
        """
         0: set b 84
         1: set c b
         2: jnz a 2
         3: jnz 1 5
         4: mul b 100
         5: sub b -100000
         6: set c b
         7: sub c -17000
         8: set f 1
         9: set d 2
        10: set e 2
        11: set g d
        12: mul g e
        13: sub g b
        14: jnz g 2
        15: set f 0
        16: sub e -1
        17: set g e
        18: sub g b
        19: jnz g -8
        20: sub d -1
        21: set g d
        22: sub g b
        23: jnz g -13
        24: jnz f 2
        25: sub h -1
        26: set g b
        27: sub g c
        28: jnz g 2
        29: jnz 1 3
        30: sub b -17
        31: jnz 1 -23
        """

        self.B = 84
        self.C = self.B

        if self.A != 0:
            self.B = self.B * 100 - 100000
            self.C = self.B - 17000

        while True:
            self.F = 1
            self.D = 2

            self.__do_more_stuff()

            while self.G != 0:  # 23
                self.__do_more_stuff()

            if self.F == 0:
                self.H += 1

            self.G = self.B - self.C  # 27

            if self.G == 0:
                return  # 29

            self.B += 17


def parse_lines(lines):
    return list(map(lambda line: line.strip().split(" "), lines))


def number_or_register(value, registers):
    register = registers.get(value)
    return register if register is not None else int(value)


def execute(value_a, lines):
    lines = parse_lines(lines)

    registers = {}
    for i in range(ord('a'), ord('h') + 1):
        registers[chr(i)] = 0

    registers['a'] = value_a
    registers['m'] = 0

    instruction = 0

    while instruction < len(lines):
        inc = 1
        parts = lines[instruction]
        register = number_or_register(parts[1], registers)

        if parts[0] == "set":
            registers[parts[1]] = number_or_register(parts[2], registers)
        elif parts[0] == "sub":
            registers[parts[1]] = register - number_or_register(parts[2], registers)
        elif parts[0] == "mul":
            registers['m'] += 1
            registers[parts[1]] = register * number_or_register(parts[2], registers)
        elif parts[0] == "jnz" and register != 0:
            inc = number_or_register(parts[2], registers)

        instruction += inc

    return registers


def test_decomp():
    registers = execute(0, from_file("inputs/23_hcf"))
    program = Program(0)
    program.run()

    test(registers['a'], program.A, "val A")
    test(registers['b'], program.B, "val B")
    test(registers['c'], program.C, "val C")
    test(registers['d'], program.D, "val D")
    test(registers['e'], program.E, "val E")
    test(registers['f'], program.F, "val F")
    test(registers['g'], program.G, "val G")
    test(registers['h'], program.H, "val H")



def main():
    # test(6724, execute(0, from_file("inputs/23_hcf"))['m'])
    # print(execute(1, from_file("inputs/23_hcf")))

    test_decomp()


if __name__ == '__main__':
    main()
