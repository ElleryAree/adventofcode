from math import floor, ceil

from Util import test, from_file


def binary_search(pattern):
    low = 0
    high = 127
    left = 0
    right = 7
    for code in pattern:
        if code == 'F':
            if high - low == 1:
                high -= 1
            else:
                high -= round((high - low) / 2)
        elif code == 'B':
            if high - low == 1:
                low += 1
            else:
                low += round((high - low) / 2)
        elif code == 'L':
            if right - left == 1:
                right -= 1
            else:
                right -= round((right - left) / 2)
        else:
            if right - left == 1:
                left += 1
            else:
                left += round((right - left) / 2)

    return low, left


def calc_seat_id(seat_location):
    row, column = seat_location
    return (row * 8) + column


def run_all(pattern):
    return calc_seat_id(binary_search(pattern))


def high_seat(patterns):
    highest_seat = 0

    for pattern in patterns:
        seat_id = run_all(pattern.strip())

        if seat_id > highest_seat:
            highest_seat = seat_id

    return highest_seat


def print_plane(patterns):
    all_seats = set(map(binary_search, patterns))

    for y in range(128):
        row = ""
        ids = []

        for x in range(4):
            if (y, x) in all_seats:
                row += "x"
            else:
                row += "o"
                ids.append(str(calc_seat_id((y, x))))

        row += " "

        for x in range(4, 8):
            if (y, x) in all_seats:
                row += "x"
            else:
                row += "o"
                ids.append(str(calc_seat_id((y, x))))

        if len(ids) > 0:
            row += ": " + (", ".join(ids))
        print(row)


def run():
    return from_file("inputs/05_boarding_passes")


if __name__ == '__main__':
    test((44, 5), binary_search("FBFBBFFRLR"))
    test(357, run_all("FBFBBFFRLR"))

    test((70, 7), binary_search("BFFFBBFRRR"))
    test(567, run_all("BFFFBBFRRR"))

    test((14, 7), binary_search("FFFBBBFRRR"))
    test(119, run_all("FFFBBBFRRR"))

    test((102, 4), binary_search("BBFFBBFRLL"))
    test(820, run_all("BBFFBBFRLL"))

    test(947, high_seat(from_file("inputs/05_boarding_passes")))

    print_plane(run())


