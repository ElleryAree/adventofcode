from Util import from_file, test


class Entry:
    def __init__(self, name):
        self.name = name
        self.size = 0

    def __str__(self):
        return "%s: %s" % (self.name, self.size)


def count(lines):
    all_dirs = []
    current_dir = None
    queue = []

    for line in lines:
        line = line.strip()

        if line.startswith("$ cd"):
            name = line[5:]

            if name == '..':
                prev_dir = queue.pop()
                prev_dir.size += current_dir.size
                current_dir = prev_dir
            else:
                queue.append(current_dir)

                current_dir = Entry(name)
                all_dirs.append(current_dir)
            continue

        if line == '$ ls':
            continue

        if line.startswith("dir"):
            continue

        parts = line.split(" ")
        size = int(parts[0])
        current_dir.size += size

    while len(queue) > 1:
        prev_dir = queue.pop()
        prev_dir.size += current_dir.size
        current_dir = prev_dir

    total_count = 0
    sizes = []
    for a_dir in all_dirs:
        sizes.append(a_dir.size)
        if a_dir.size <= 100000:
            total_count += a_dir.size

    total_space = 70000000
    target_space = 30000000
    available_space = total_space - current_dir.size
    to_free = target_space - available_space

    min_dir = 0
    for size in sorted(sizes, key=lambda a: -a):
        if size >= to_free:
            min_dir = size
        else:
            break

    return total_count, min_dir


def run():
    return count(from_file("inputs/07_dirs"))[1]


def main():
    test(95437, count(from_file("test_inputs/07_dirs"))[0])
    test(1084134, count(from_file("inputs/07_dirs"))[0])

    test(24933642, count(from_file("test_inputs/07_dirs"))[1])
    print(run())


if __name__ == '__main__':
    main()
