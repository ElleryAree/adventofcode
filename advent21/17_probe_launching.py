from Util import test


test_input = (20, 30), (-10, -5)
puzzle_input = (102, 157), (-146, -90)


def simulate_speed(x, y, dx, dy):
    return x + dx, y + dy, dx - 1 if dx > 0 else 0, dy - 1


def check_sim_x(dx, target_x):
    x = 0
    target_min_x, target_max_x = target_x

    while True:
        x += dx
        dx = dx - 1 if dx > 0 else 0

        if target_min_x <= x <= target_max_x:
            return True

        if x > target_max_x or (dx == 0 and x < target_min_x):
            return False
    pass


def check_sim_y(dx, dy, target_x, target_y):
    x = 0
    y = 0
    t = 0

    target_min_x, target_max_x = target_x
    target_min_y, target_max_y = target_y

    max_y = 0

    while True:
        x, y, dx, dy = simulate_speed(x, y, dx, dy)
        t += 1

        if y > max_y:
            max_y = y

        if target_min_x <= x <= target_max_x and target_min_y <= y <= target_max_y:
            return True, max_y

        if x > target_max_x or y < target_min_y:
            return False, max_y


def try_sims_x(target):
    target_x, target_y = target
    hits = []

    for dx in range(1, target_x[1] + 1):
        hit = check_sim_x(dx, target_x)
        if hit:
            hits.append(dx)

    return hits


def try_sims_y(target, dx):
    target_x, target_y = target

    max_max_y = 0
    has_hit = False

    hits = 0

    for dy in range(target_y[0], 1000):
        hit, max_y = check_sim_y(dx, dy, target_x, target_y)

        if not has_hit and hit:
            has_hit = True

        if hit:
            hits += 1
            if max_y > max_max_y:
                max_max_y = max_y

    return max_max_y, hits


def try_sims(target):
    hit_set = 0
    hits = try_sims_x(target)
    max_y = 0
    for dx in hits:
        y, this_hits = try_sims_y(target, dx)
        hit_set += this_hits

        if y > max_y:
            max_y = y

    return max_y, hit_set


def run():
    return try_sims(puzzle_input)[1]


def main():
    hit_points = {
        (23, -10), (25, -9), (27, -5), (29, -6), (22, -6), (21, -7), (9, 0), (27, -7), (24, -5),
        (25, -7), (26, -6), (25, -5), (6, 8), (11, -2), (20, -5), (29, -10), (6, 3), (28, -7),
        (8, 0), (30, -6), (29, -8), (20, -10), (6, 7), (6, 4), (6, 1), (14, -4), (21, -6),
        (26, -10), (7, -1), (7, 7), (8, -1), (21, -9), (6, 2), (20, -7), (30, -10), (14, -3),
        (20, -8), (13, -2), (7, 3), (28, -8), (29, -9), (15, -3), (22, -5), (26, -8), (25, -8),
        (25, -6), (15, -4), (9, -2), (15, -2), (12, -2), (28, -9), (12, -3), (24, -6), (23, -7),
        (25, -10), (7, 8), (11, -3), (26, -7), (7, 1), (23, -9), (6, 0), (22, -10), (27, -6),
        (8, 1), (22, -8), (13, -4), (7, 6), (28, -6), (11, -4), (12, -4), (26, -9), (7, 4),
        (24, -10), (23, -8), (30, -8), (7, 0), (9, -1), (10, -1), (26, -5), (22, -9), (6, 5),
        (7, 5), (23, -6), (28, -10), (10, -2), (11, -1), (20, -9), (14, -2), (29, -7), (13, -3),
        (23, -5), (24, -8), (27, -9), (30, -7), (28, -5), (21, -10), (7, 9), (6, 6), (21, -5),
        (27, -10), (7, 2), (30, -9), (21, -8), (22, -7), (24, -9), (20, -6), (6, 9), (29, -5),
        (8, -2), (27, -8), (30, -5), (24, -7),
    }

    actual_points = try_sims(test_input)

    test(45, actual_points[0])
    test(len(hit_points), actual_points[1])

    test(10585, try_sims(puzzle_input)[0])
    test(5247, run())


if __name__ == '__main__':
    main()
