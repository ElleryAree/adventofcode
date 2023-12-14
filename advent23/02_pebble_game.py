from Util import test, from_file


def parse_set(set_line):
    colors = set_line.split(", ")

    reds = 0
    greens = 0
    blues = 0

    for color in colors:
        parts = color.split(" ")
        if parts[1] == 'red':
            reds += int(parts[0])
        if parts[1] == 'green':
            greens += int(parts[0])
        if parts[1] == 'blue':
            blues += int(parts[0])

    return reds, greens, blues


def parse_game(game_line):
    name, sets = game_line.split(": ")
    name = int(name.split(" ")[1])
    sets = sets.split("; ")

    set_stones = []
    for set_line in sets:
        set_stones.append(parse_set(set_line))

    return name, set_stones


def game_is_valid(max_blues, max_greens, max_reds, pebbles):
    for reds, greens, blues in pebbles:
        if reds > max_reds or greens > max_greens or blues > max_blues:
            return False
    return True


def check_stones(max_reds, max_greens, max_blues, lines):
    good = 0
    for line in lines:
        line = line.strip()

        name, pebbles = parse_game(line)

        if game_is_valid(max_blues, max_greens, max_reds, pebbles):
            good += name

    return good


def find_min(lines):
    total = 0
    for line in lines:
        line = line.strip()

        name, pebbles = parse_game(line)

        max_red = 0
        max_green = 0
        max_blue = 0

        for reds, greens, blues in pebbles:
            if reds > max_red:
                max_red = reds
            if greens > max_green:
                max_green = greens
            if blues > max_blue:
                max_blue = blues

        total += max_red * max_green * max_blue

    return total


def main():
    test(8, check_stones(12, 13, 14, from_file("test_inputs/02_pebble_game")))
    test(2164, check_stones(12, 13, 14, from_file("inputs/02_pebble_game")))

    test(2286, find_min(from_file("test_inputs/02_pebble_game")))
    print(find_min(from_file("inputs/02_pebble_game")))


if __name__ == '__main__':
    main()
