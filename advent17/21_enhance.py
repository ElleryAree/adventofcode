from Util import test, from_file


def invert(source):
    source = list(source)
    for i in range(int(len(source) / 2)):
        temp = source[i]
        source[i] = source[len(source) - i - 1]
        source[len(source) - i - 1] = temp
    return source


def all_inverted(pattern, enhance, enhancements):
    enhancements[tuple(pattern)] = enhance
    enhancements[tuple(invert(pattern))] = enhance

    inverted = []
    for line in pattern:
        inverted.append("".join(invert(line)))

    enhancements[tuple(inverted)] = enhance
    enhancements[tuple(invert(inverted))] = enhance


def rotate(pattern):
    rotated = ["" for _ in range(len(pattern))]
    for y, line in enumerate(pattern):
        for x, c in enumerate(line):
            rotated[x] += c
    return rotated


def build_rules(source, enhancements):
    pattern, enhance = source.split(" => ")
    pattern = pattern.split("/")
    enhance = enhance.split("/")

    for _ in range(4):
        all_inverted(pattern, enhance, enhancements)
        pattern = rotate(pattern)

    return enhancements


def parce_book(lines):
    enhancements = {}

    for line in lines:
        build_rules(line.strip(), enhancements)

    return enhancements


def break_into_pieces(grid):
    if len(grid) % 2 == 0:
        scale = 2
    else:
        scale = 3

    pieces = int(len(grid) / scale)
    all_pieces = []

    for y in range(pieces):
        line = []
        for x in range(pieces):
            broken = []
            for i in range(scale):
                broken.append(grid[y * scale + i][x * scale: x * scale + scale])
            line.append(broken)
        all_pieces.append(line)

    return all_pieces


def enhance_step(grid, enhancements):
    pieces = break_into_pieces(grid)

    enhanced_grid = []
    for row in pieces:
        enhanced_row = []
        row = [enhancements[tuple(line)] for line in row]

        for _ in range(len(row[0])):
            enhanced_row.append("")

        for line in row:
            for y, pixel in enumerate(line):
                enhanced_row[y] += line[y]

        enhanced_grid.extend(enhanced_row)

    return enhanced_grid


def run_enhance(start, iterations, lines):
    enhancements = parce_book(lines)
    grid = start

    for i in range(iterations):
        grid = enhance_step(grid, enhancements)

    count = 0
    for line in grid:
        for c in line:
            if c == '#':
                count += 1

    return count



def main():
    start = [".#.", "..#", "###"]

    test(12, run_enhance(start, 2, from_file("test_inputs/21_enhance")))
    test(142, run_enhance(start, 5, from_file("inputs/21_enhance")))
    print(run_enhance(start, 18, from_file("inputs/21_enhance")))


if __name__ == '__main__':
    main()
