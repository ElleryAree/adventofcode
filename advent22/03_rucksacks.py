from Util import test, from_file


def separate_comps(line):
    comp_len = len(line) / 2
    comp_1 = line[0:comp_len]
    comp_2 = line[comp_len:]

    return comp_1, comp_2


def compare_contents(comp_1, comp_2):
    inters = set()

    for c in comp_1:
        if c in comp_2:
            inters.add(c)

    return inters


def compare_badges(sacks):
    items = {}

    for i, sack in enumerate(sacks):
        for c in sack:
            count = items.get(c, set())
            count.add(i)
            items[c] = count

    for c, count in items.items():
        if len(count) == 3:
            return c


def count_inters(inters):
    count = 0

    for c in inters:
        value = ord(c)

        if 'A' <= c <= 'Z':
            value -= ord('A')
            value += 27
        else:
            value -= ord('a')
            value += 1

        count += value

    return count


def count_rucksacks(lines):
    total_count = 0
    for line in lines:
        line = line.strip()

        comp_1, comp_2 = separate_comps(line)
        inters = compare_contents(comp_1, comp_2)
        total_count += count_inters(inters)

    return total_count


def count_badges(lines):
    total_count = 0

    for i in range(0, len(lines), 3):
        first = lines[i].strip()
        second = lines[i + 1].strip()
        third = lines[i + 2].strip()

        item = compare_badges((first, second, third))
        total_count += count_inters((item, ))

    return total_count


def run():
    return count_badges(from_file("inputs/03_rucksacks"))


def main():
    test(157, count_rucksacks(from_file("test_inputs/03_rucksacks")))
    test(7568, count_rucksacks(from_file("inputs/03_rucksacks")))

    test(70, count_badges(from_file("test_inputs/03_rucksacks")))
    print(run())


if __name__ == '__main__':
    main()