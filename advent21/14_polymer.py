from Util import test, from_file


def parse_input(lines):
    start_pattern = lines[0].strip()

    replacements = {}
    for line in lines[2:]:
        pair, insert = line.strip().split(" -> ")

        start = pair[0]
        end = pair[1]

        if start not in replacements:
            replacements[start] = {}

        replacements[start][end] = insert

    return start_pattern, replacements


def merge_frequencies(first, second):
    merged = {}

    for c, count in first.items():
        merged[c] = count

    for c, count in second.items():
        prev_count = merged.get(c, 0)
        merged[c] = prev_count + count

    return merged


def replace_rec(pair, replacements, cache, steps):
    if steps == 0:
        if pair[0] == pair[1]:
            return {pair[0]: 2}
        else:
            return {pair[0]: 1, pair[1]: 1}

    first, second = pair
    key = first, second, steps

    if key in cache:
        return cache[key]

    insert = replacements[first][second]

    first_score = replace_rec((first, insert), replacements, cache, steps - 1)
    second_score = replace_rec((insert, second), replacements, cache, steps - 1)

    merged = merge_frequencies(first_score, second_score)
    merged[insert] -= 1
    cache[key] = merged

    return merged


def replace_clever(start_pattern, replacements, steps):
    pairs = []
    for i in range(len(start_pattern) - 1):
        first = start_pattern[i]
        second = start_pattern[i + 1]

        pairs.append((first, second))

    cache = {}
    final_score = {}

    for i, pair in enumerate(pairs):
        score = replace_rec(pair, replacements, cache, steps)
        if i > 0:
            score[pair[0]] -= 1
        final_score = merge_frequencies(final_score, score)

    return final_score


def min_max(frequencies):
    max_count = 0
    min_count = 100000000000000000000000

    for count in frequencies.values():
        if count > max_count:
            max_count = count
        if count < min_count:
            min_count = count

    return min_count, max_count


def run_iters(lines, steps):
    start_pattern, replacements = parse_input(lines)

    frequencies = replace_clever(start_pattern, replacements, steps)
    min_count, max_count = min_max(frequencies)

    return max_count - min_count


def run():
    return run_iters(from_file("inputs/14_polymer"), 40)


def main():
    test(1588, run_iters(from_file("test_inputs/14_polymer"), 10))
    test(3230, run_iters(from_file("inputs/14_polymer"), 10))

    test(2188189693529, run_iters(from_file("test_inputs/14_polymer"), 40))
    test(3542388214529, run())


if __name__ == '__main__':
    main()
