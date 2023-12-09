from Util import test, from_file


def parse(lines):
    return [list(map(int, line.strip().split())) for line in lines]


def add_layer(seq):
    is_zeroes = True
    layer = []
    for i in range(len(seq) - 1):
        item = seq[i + 1] - seq[i]
        is_zeroes = is_zeroes and item == 0
        layer.append(item)

    return layer, is_zeroes


def add_all_layers(seq):
    layers = [seq]

    while True:
        current_layer = layers[-1]
        next_layer, is_zeroes = add_layer(current_layer)
        layers.append(next_layer)

        if is_zeroes:
            break

    return layers


def extend_layers_backwards(layers):
    layers[-1].insert(0, 0)

    for i in range(len(layers) - 2, -1, -1):
        layer = layers[i]
        diff = layers[i + 1][0]
        layer.insert(0, layer[0] - diff)

    return layers[0][0]


def extend_layers(layers):
    layers[-1].append(0)

    for i in range(len(layers) - 2, -1, -1):
        layer = layers[i]
        diff = layers[i + 1][-1]
        layer.append(layer[-1] + diff)

    return layers[0][-1]


def calculate(extend_f, lines):
    total = 0
    for seq in parse(lines):
        all_lines = add_all_layers(seq)
        total += extend_f(all_lines)
    return total


def run():
    print(calculate(extend_layers_backwards, from_file("inputs/09_oasis")))


def main():
    test(114, calculate(extend_layers, from_file("test_inputs/09_oasis")))
    test(1969958987, calculate(extend_layers, from_file("inputs/09_oasis")))

    test(2, calculate(extend_layers_backwards, from_file("test_inputs/09_oasis")))
    run()


if __name__ == '__main__':
    main()
