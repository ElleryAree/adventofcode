from Util import test


def spin(skip, iterations=2017, answer_position=None):
    memory = [0]
    position = 0
    for i in range(iterations):
        position = (position + skip) % len(memory) + 1
        memory.insert(position, i + 1)

    if answer_position is None:
        answer_position = position + 1
    return memory[answer_position]


def spin_virtual(skip, iterations):
    position = 0
    value = 0

    for i in range(iterations):
        position = (position + skip) % (i + 1) + 1
        if position == 1:
            value = i + 1

    return value


def main():
    test(638, spin(3))
    test(638, spin(354))

    test(spin(3, 15, 1), spin_virtual(3, 15))
    print(spin_virtual(354, 50000001))


if __name__ == '__main__':
    main()
