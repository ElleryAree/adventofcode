from copy import copy

from Util import test

small_test_input = [
    'start-A',
    'start-b',
    'A-c',
    'A-b',
    'b-d',
    'A-end',
    'b-end'
]

med_test_input = [
    'dc-end',
    'HN-start',
    'start-kj',
    'dc-start',
    'dc-HN',
    'LN-dc',
    'HN-end',
    'kj-sa',
    'kj-HN',
    'kj-dc'
]

large_test_input = [
    'fs-end',
    'he-DX',
    'fs-he',
    'start-DX',
    'pj-DX',
    'end-zg',
    'zg-sl',
    'zg-pj',
    'pj-he',
    'RW-he',
    'fs-DX',
    'pj-RW',
    'zg-RW',
    'start-pj',
    'he-WI',
    'zg-he',
    'pj-fs',
    'start-RW'
]


input = [
    'fw-ll',
    'end-dy',
    'tx-fw',
    'tx-tr',
    'dy-jb',
    'ZD-dy',
    'dy-BL',
    'dy-tr',
    'dy-KX',
    'KX-start',
    'KX-tx',
    'fw-ZD',
    'tr-end',
    'fw-jb',
    'fw-yi',
    'ZD-nr',
    'start-fw',
    'tx-ll',
    'll-jb',
    'yi-jb',
    'yi-ll',
    'yi-start',
    'ZD-end',
    'ZD-jb',
    'tx-ZD',
]


class Node:
    def __init__(self, path=(), visited=None, visited_twice=False):
        self.path = path
        self.__visited = set() if visited is None else visited
        self.__visited_twice = visited_twice

    def with_next(self, next_node):
        visited_twice = self.__visited_twice or (next_node.islower() and next_node in self.__visited)
        visited = copy(self.__visited)
        visited.add(next_node)

        return Node(self.path + (next_node, ), visited, visited_twice)

    def is_visited(self, node):
        if not self.__visited_twice:
            return False

        return node.islower() and node in self.__visited

    def __str__(self):
        return "%s, %s" % (','.join(self.path), self.__visited_twice)


def build_nodes(lines):
    def add_nodes(node_start, node_end):
        if node_end == 'start' or node_start == 'end':
            return

        if node_start not in nodes:
            nodes[node_start] = []

        nodes[node_start].append(node_end)

    nodes = {}

    for line in lines:
        start, end = line.split('-')

        add_nodes(start, end)
        add_nodes(end, start)

    return nodes


def find_path(nodes):
    paths = []
    queue = [(Node(), 'start')]

    while len(queue) > 0:
        node, next_node = queue.pop()

        if next_node == 'end':
            paths.append(node.path)
            # print("%s,end" % ",".join(node.path))
            continue

        if node.is_visited(next_node):
            continue

        node = node.with_next(next_node)
        for following_node in nodes[next_node]:
            queue.append((node, following_node))

    return len(paths)


def do_run(lines):
    return find_path(build_nodes(lines))


def run():
    return do_run(input)


def main():
    test(36, do_run(small_test_input))
    test(103, do_run(med_test_input))
    test(3509, do_run(large_test_input))
    test(117509, run())


if __name__ == '__main__':
    main()
