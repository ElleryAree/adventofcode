from Util import test

def fill_part_1(i, c, spiral):
    return i

fill_directions = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1))
def fill_part_2(i, c, spiral):
    x, y = c
    total = 0
    for dx, dy in fill_directions:
        total += spiral.get((x + dx, y + dy), 0)
    return total

def condition_part_1(i, max_number):
    return i != max_number

def condition_part_2(i, max_number):
    return i <= max_number

def generate_spiral(max_number, fill, condition):
    spiral = {(0, 0): 1}
    inverted_spiral = {1: (0, 0)}
    directions = ((1, 0), (0, -1), (-1, 0), (0, 1))
    direction_id = 3

    x, y = 0, 0
    i = 2
    value = 2

    while condition(value, max_number):
        next_id = (direction_id + 1) % 4

        dx, dy = directions[direction_id]
        n_dx, n_dy = directions[next_id]

        key = x + dx, y + dy
        next_key = x + n_dx, y + n_dy

        if next_key not in spiral:
            c = next_key
            direction_id = next_id
        else:
            c = key

        value = fill(i, c, spiral)

        spiral[c] = value
        inverted_spiral[value] = c

        x, y = c
        i += 1

    return inverted_spiral, value


def generate_and_find(max_value, needle):
    inverted_spiral = generate_spiral(max_value, fill_part_1, condition_part_1)[0]

    x, y = inverted_spiral[needle]
    return abs(x) + abs(y)


def generate_and_find_max(max_value):
    return generate_spiral(max_value, fill_part_2, condition_part_2)[-1]


def main():
    test(0, generate_and_find(25, 1))
    test(3, generate_and_find(25, 12))
    test(2, generate_and_find(25, 23))
    test(31, generate_and_find(1025, 1024))

    test(371, generate_and_find(368079, 368078))
    print(generate_and_find_max(368078))


if __name__ == '__main__':
    main()
