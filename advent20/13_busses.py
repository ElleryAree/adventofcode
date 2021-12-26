from Util import test, from_file


def prev_timestamp(bus_id, start) -> int:
    return start - (start % bus_id)


def next_timestamp(bus_id, start) -> int:
    return prev_timestamp(bus_id, start) + bus_id


def process_busses(busses, start) -> int:
    min_time = None
    min_id = None
    for bus in busses:
        time = next_timestamp(bus, start)
        if min_time is None or time < min_time:
            min_time = time
            min_id = bus

    return (min_time - start) * min_id


def parse_input(lines):
    start = int(lines[0].strip())
    all_busses = lines[1].strip().split(",")
    busses = list(map(int, filter(lambda bus: bus != 'x', all_busses)))

    return start, busses


def parse_input_for_sequence(lines):
    busses = []

    for i, bus in enumerate(lines[1].strip().split(",")):
        if bus == 'x':
            continue

        busses.append((i, int(bus)))

    return busses


def is_sequence_1(timestamp, bus):
    i, bus = bus
    rem = (timestamp + i) % bus

    return rem == 0


def is_sequence_2(timestamp, bus1, bus2):
    return is_sequence_1(timestamp, bus1) and is_sequence_1(timestamp, bus2)


def is_sequence_all(timestamp, busses):
    for bus in busses:
        if not is_sequence_1(timestamp, bus):
            return False

    return True


def find_sequence(start, inc, bus):
    timestamp = start
    while True:
        if is_sequence_1(timestamp, bus):
            return timestamp

        timestamp += inc


def find_sequence_3(busses):
    busses = list(sorted(busses, key=lambda b: -b[1]))

    inc = 1
    start = 0
    first_time = 0

    for bus in busses:
        first_time = find_sequence(start, inc, bus)
        second_time = find_sequence(first_time + inc, inc, bus)

        diff = second_time - first_time

        inc = diff
        start = first_time

    return first_time


def run_one(lines) -> int:
    start, busses = parse_input(lines)

    return process_busses(busses, start)


def run_sequence(lines, f):
    busses = parse_input_for_sequence(lines)

    return f(busses)


def run():
    return run_sequence(from_file("inputs/13_busses"), find_sequence_3)


if __name__ == '__main__':
    test_input = ["939\n", "7,13,x,x,59,x,31,19\n"]

    test(295, run_one(test_input))
    test(2406, run_one(from_file("inputs/13_busses")))

    test(1068781, run_sequence(test_input, find_sequence_3))

    test(3417, run_sequence(["", "17,x,13,19"], find_sequence_3))
    test(754018, run_sequence(["", "67,7,59,61"], find_sequence_3))
    test(779210, run_sequence(["", "67,x,7,59,61"], find_sequence_3))
    test(1261476, run_sequence(["", "67,7,x,59,61"], find_sequence_3))
    test(1202161486, run_sequence(["", "1789,37,47,1889"], find_sequence_3))

    test(225850756401039, run())
