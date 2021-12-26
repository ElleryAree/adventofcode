import time

from Util import test


class Memento:
    def __init__(self, turn):
        self.__first = turn
        self.__second = turn

    def update(self, turn):
        self.__first = self.__second
        self.__second = turn

    def say(self):
        return self.__second - self.__first


def update_memory(memory, say, turn):
    last_turn = memory.get(say)

    if last_turn is None:
        memory[say] = (turn,)
    elif len(last_turn) > 0:
        memory[say] = (last_turn[-1], turn)


def turns(numbers, max_turns=2020):
    a_turn = 1
    memory = {}
    last = None

    for number in numbers:
        memory[number] = Memento(a_turn)
        last = number
        a_turn += 1

    for turn in range(a_turn, max_turns + 1):
        last_memento = memory.get(last)
        if last_memento is None:
            last_memento = Memento(turn)
            memory[last] = last_memento

        last = last_memento.say()

        next_memento = memory.get(last)
        if next_memento is not None:
            next_memento.update(turn)
        else:
            next_memento = Memento(turn)
            memory[last] = next_memento

    return last


def run():
    return turns([1, 20, 8, 12, 0, 14], 30000000)


if __name__ == '__main__':
    test(436, turns([0, 3, 6], 2020))
    # test(1, turns([1, 3, 2]))
    # test(10, turns([2, 1, 3]))
    # test(27, turns([1, 2, 3]))
    # test(78, turns([2, 3, 1]))
    # test(438, turns([3, 2, 1]))
    # test(1836, turns([3, 1, 2]))
    test(492, turns([1, 20, 8, 12, 0, 14]))

    # test(175594, turns([0, 3, 6], 30000000))
    # test(2578, turns([1, 3, 2], 30000000))
    # test(3544142, turns([2, 1, 3], 30000000))
    # test(261214, turns([1, 2, 3], 30000000))
    # test(6895259, turns([2, 3, 1], 30000000))
    # test(18, turns([3, 2, 1], 30000000))
    # test(362, turns([3, 1, 2], 30000000))

    start = time.time()
    test(63644, run())
    print("Elapsed: %d" % (time.time() - start))
