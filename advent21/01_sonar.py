from Util import test, from_file


class Window:
    def __init__(self):
        self.__data = []

    def add(self, item):
        if len(self.__data) < 2:
            self.__data.append(item)
            return None

        if len(self.__data) == 2:
            self.__data.append(item)
            return sum(self.__data)

        self.__data[0] = self.__data[1]
        self.__data[1] = self.__data[2]
        self.__data[2] = item

        return sum(self.__data)


def count_depth(readings, f=lambda item: item):
    count = 0
    prev = None

    for reading in readings:
        reading = f(int(reading.strip()))
        if prev is not None and prev < reading:
            count += 1
        prev = reading

    return count


def count_window(readings):
    window = Window()
    return count_depth(readings, window.add)


def run():
    return count_window(from_file("inputs/01_sonar"))


def main():
    test(7, count_depth(("199", "200", "208", "210", "200", "207", "240", "269", "260", "263",)))
    test(1688, count_depth(from_file("inputs/01_sonar")))

    test(5, count_window(("199", "200", "208", "210", "200", "207", "240", "269", "260", "263",)))
    print(run())


if __name__ == '__main__':
    main()
