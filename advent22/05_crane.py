from Util import from_file, test


def parse_stack(lines):
    buffer = []

    while(True):
        line = lines.pop(0)

        if '1' in line:
            buckets = [[] for _ in filter(lambda l: l != '', map(lambda l: l.strip(), line.split(' ')))]
            lines.pop(0)
            break

        buffer.append(line)

    for line in buffer:
        for i in range(1, len(line) - 1, 4):
            if line[i] == ' ':
                continue

            buckets[int(i / 4)].append(line[i])

    return buckets


def move_stuff(buckets, amount, stack_from, stack_to, is_9000):
    backet_from = buckets[stack_from]
    backet_to = buckets[stack_to]

    buckets[stack_from] = backet_from[amount:]
    buckets[stack_to] = backet_from[0:amount]
    if is_9000:
        buckets[stack_to].reverse()
    buckets[stack_to].extend(backet_to)


def tops(buckets):
    return "".join([bucket[0] for bucket in buckets])


def process_input(lines, is_9000):
    buckets = parse_stack(lines)

    for line in lines:
        parts = line.strip().split(" ")

        amount = parts[1]
        stack_from = parts[3]
        stack_to = parts[5]

        move_stuff(buckets, int(amount), int(stack_from) - 1, int(stack_to) - 1, is_9000=is_9000)

    return tops(buckets)


def run():
    return process_input(from_file("inputs/05_crane"), is_9000=False)


def main():
    test("CMZ", process_input(from_file("test_inputs/05_crane"), is_9000=True))
    test('MQSHJMWNH', process_input(from_file("inputs/05_crane"), is_9000=True))

    test("MCD", process_input(from_file("test_inputs/05_crane"), is_9000=False))
    print(run())


if __name__ == '__main__':
    main()
