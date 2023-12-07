from Util import from_file, test


def parse(lines):
    times = map(int, lines[0].split(":")[1].split())
    durations = map(int, lines[1].split(":")[1].split())

    return list(zip(times, durations))


def parse_part_2(lines):
    times = int(lines[0].split(":")[1].replace(" ", "").strip())
    durations = int(lines[1].split(":")[1].replace(" ", "").strip())

    return ((times, durations), )


def simulate_races(parser, lines):
    races = parser(lines)

    total = 1

    for (time, max_distance) in races:
        races_won = 0
        for t in range(time):
            speed = t
            distance = (time - t) * speed

            if distance > max_distance:
                races_won += 1
            elif races_won > 0:
                break

        total *= races_won

    return total


def run():
    print(simulate_races(parse_part_2, from_file("inputs/06_boat_races")))


def main():
    test(288, simulate_races(parse, from_file("test_inputs/06_boat_races")))
    test(4568778, simulate_races(parse, from_file("inputs/06_boat_races")))

    test(71503, simulate_races(parse_part_2, from_file("test_inputs/06_boat_races")))
    run()


if __name__ == '__main__':
    main()
