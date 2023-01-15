from Util import test, from_file


def parse(lines):
    layers = {}
    max_layer = 0
    for line in lines:
        layer, size = line.strip().split(": ")
        layer = int(layer)
        layers[layer] = int(size)
        max_layer = layer

    return layers, max_layer


def calculate_pos(scanner_pos, size):
    scaled_scanner = scanner_pos % (size * 2 - 2)

    if scaled_scanner >= size:
        scaled_scanner = 2 * size - scaled_scanner - 2

    return scaled_scanner


def run(data, start, should_stop):
    layers, target = data

    scanner_pos = start
    caught_count = 0

    for package_pos in range(target + 1):
        size = layers.get(package_pos, -1)
        if size > 0:
            if calculate_pos(scanner_pos, size) == 0:
                if should_stop:
                    return -1

                caught_count += scanner_pos * size

        scanner_pos += 1

    return caught_count


def part_1(lines):
    return run(parse(lines), 0, False)


def part_2(lines):
    data = parse(lines)

    delay = 0
    while True:
        severity = run(data, delay, True)
        if severity == 0:
            return delay
        delay += 1



def main():
    test(24, part_1(from_file("test_inputs/13_scanner")))
    test(2688, part_1(from_file("inputs/13_scanner")))

    test(10, part_2(from_file("test_inputs/13_scanner")))
    print(part_2(from_file("inputs/13_scanner")))


if __name__ == '__main__':
    main()
