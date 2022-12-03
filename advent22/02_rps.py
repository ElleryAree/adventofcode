from Util import test, from_file

rock = 'Rock'
paper = 'Paper'
sci = 'Scissors'

out_lost = 'lost'
out_draw = 'draw'
out_win = 'win'


def map_fist_part(key):
    if key == 'A':
        return rock
    if key == 'B':
        return paper
    return sci


def map_second_part(key):
    if key == 'X':
        return rock
    if key == 'Y':
        return paper
    return sci


def map_second_part_for_part_two(key):
    if key == 'X':
        return out_lost
    if key == 'Y':
        return out_draw
    return out_win


def map_shape_score(shape):
    if shape == rock:
        return 1
    if shape == paper:
        return 2
    return 3


def map_outcome_score(outcome):
    if outcome == out_lost:
        return 0
    if outcome == out_draw:
        return 3
    return 6


def map_outcome_to_shape(their_shape, outcome):
    if outcome == out_draw:
        return their_shape

    if outcome == out_lost:
        if their_shape == rock:
            return sci
        if their_shape == paper:
            return rock
        if their_shape == sci:
            return paper

    if outcome == out_win:
        if their_shape == rock:
            return paper
        if their_shape == paper:
            return sci
        if their_shape == sci:
            return rock


def rule_round(my_shape, their_shape):
    if my_shape == their_shape:
        return out_draw

    if my_shape == rock:
        if their_shape == paper:
            return out_lost
        if their_shape == sci:
            return out_win

    if my_shape == paper:
        if their_shape == rock:
            return out_win
        if their_shape == sci:
            return out_lost

    if my_shape == sci:
        if their_shape == paper:
            return out_win
        if their_shape == rock:
            return out_lost


def run_strategy_step(step):
    step = step.split(' ')
    if len(step) != 2:
        return 0

    their_shape = map_fist_part(step[0])
    my_shape = map_second_part(step[1])
    outcome = rule_round(my_shape, their_shape)

    return map_shape_score(my_shape) + map_outcome_score(outcome)


def run_strategy_step_part_two(step):
    step = step.split(' ')
    if len(step) != 2:
        return 0

    their_shape = map_fist_part(step[0])
    outcome = map_second_part_for_part_two(step[1])
    my_shape = map_outcome_to_shape(their_shape, outcome)

    return map_shape_score(my_shape) + map_outcome_score(outcome)


def run_strategy(strategy, step_f):
    total_score = 0
    for step in strategy:
        total_score += step_f(step.strip())

    return total_score


def run():
    return run_strategy(from_file("inputs/02_rps"), run_strategy_step_part_two)


def main():
    test_strategy = """
    A Y
    B X
    C Z
    """

    test(15, run_strategy(test_strategy.split('\n'), run_strategy_step))
    test(13052, run_strategy(from_file("inputs/02_rps"), run_strategy_step))

    test(12, run_strategy(test_strategy.split('\n'), run_strategy_step_part_two))
    print(run())


if __name__ == '__main__':
    main()
