from Util import test


class Memory:
    def __init__(self, configuration):
        self.__items = list(configuration)

    def __find_max(self):
        max_value = 0
        max_i = 0

        for i, value in enumerate(self.__items):
            if value > max_value:
                max_value = value
                max_i = i

        return max_i, max_value

    def redistribute(self):
        i, max_value = self.__find_max()

        self.__items[i] = 0

        while max_value > 0:
            i = (i + 1) % len(self.__items)
            self.__items[i] += 1
            max_value -= 1

    def as_tuple(self):
        return tuple(self.__items)


def find_repeat(configuration, find_loop):
    memory = Memory(configuration)
    visited = {}

    steps = 0

    while True:
        memory_tuple = memory.as_tuple()
        if memory_tuple in visited:
            if find_loop:
                return steps - visited[memory_tuple]

            return steps

        visited[memory_tuple] = steps

        steps += 1
        memory.redistribute()


def main():
    input_data = (5, 1, 10, 0, 1, 7, 13, 14, 3, 12, 8, 10, 7, 12, 0, 6)

    test(5, find_repeat((0, 2, 7, 0), False))
    test(5042, find_repeat(input_data, False))

    test(4, find_repeat((0, 2, 7, 0), True))
    print(find_repeat(input_data, True))


if __name__ == '__main__':
    main()
