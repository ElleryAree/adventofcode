from Util import test, from_file


def add_to(value, pins, elements):
    all_pins = elements.get(value)
    if all_pins is None:
        all_pins = []
        elements[value] = all_pins
    all_pins.append(pins)



def parse(lines):
    elements = {}
    starts = []
    elements_list = []

    for line in lines:
        left, right = line.strip().split("/")
        pins = (int(left), int(right))

        elements_list.append(pins)
        add_to(pins[0], pins, elements)
        add_to(pins[1], pins, elements)

        if pins[0] == 0 or pins[1] == 0:
            starts.append(pins)

    return elements, elements_list, starts


def calculate_strength(bridge):
    strength = 0
    for pins in bridge:
        strength += pins[0] + pins[1]
    return strength


def build_bridges(lines):
    elements, elements_list, starts = parse(lines)

    frontier = []
    for start in starts:
        second = start[1] if start[0] == 0 else start[0]
        frontier.append((second, (start,)))

    max_strength = 0
    max_length = 0
    best_bridge = None

    while len(frontier) > 0:
        pin, bridge = frontier.pop()

        added = 0
        for pins in elements.get(pin, []):
            if pins in bridge:
                continue

            added += 1

            other = pins[0] if pins[1] == pin else pins[1]
            frontier.append((other, bridge + (pins,)))

        if added == 0:
            strength = calculate_strength(bridge)

            if len(bridge) > max_length:
                max_length = len(bridge)
                best_bridge = bridge
            elif len(bridge) == max_length:
                if strength > calculate_strength(best_bridge):
                    best_bridge = bridge


            if strength > max_strength:
                max_strength = strength

    return max_strength, calculate_strength(best_bridge)


def main():
    test_best_str, test_best_len = build_bridges(from_file("test_inputs/24_bridge"))
    test(31, test_best_str)
    test(19, test_best_len)

    best_str, best_len = build_bridges(from_file("inputs/24_bridge"))
    test(1511, best_str)
    print(best_len)


if __name__ == '__main__':
    main()
