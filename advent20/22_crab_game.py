from collections import deque

from Util import test, from_file


class State:
    def __init__(self, game, game_round, first_deck, second_deck, first_states, second_states):
        self.game = game
        self.round = game_round

        self.first_deck = first_deck
        self.second_deck = second_deck

        self.first_states = first_states
        self.second_states = second_states


def parse_input(lines):
    first_player = deque()
    second_player = deque()
    deck = first_player

    for line in lines:
        line = line.strip()

        if line == '':
            deck = second_player
            continue

        if line[0] == 'P':
            continue

        deck.append(int(line))

    return first_player, second_player


def play_game(first_player, second_player):
    while len(first_player) > 0 and len(second_player) > 0:
        first = first_player.popleft()
        second = second_player.popleft()

        if first > second:
            first_player.append(first)
            first_player.append(second)
        else:
            second_player.append(second)
            second_player.append(first)

    return second_player if len(first_player) == 0 else first_player


def play_recursive_game(winner, game, turn, first_player, second_player, first_states, second_states, queue):
    while len(first_player) > 0 and len(second_player) > 0:
        first_snapshot = deck_snapshot(first_player)
        second_snapshot = deck_snapshot(second_player)

        if winner is None and (first_snapshot in first_states or second_snapshot in second_states):
            return 1, None

        first_states.add(first_snapshot)
        second_states.add(second_snapshot)

        turn += 1

        first_len_before_pop = len(first_player)
        second_len_before_pop = len(second_player)

        first = first_player.popleft()
        second = second_player.popleft()

        if winner is None and (first < first_len_before_pop and second < second_len_before_pop):
            state = State(game, turn - 1, first_player.copy(), second_player.copy(), first_states, second_states)
            state.first_deck.appendleft(first)
            state.second_deck.appendleft(second)
            queue.append(state)

            for _ in range(len(first_player) - first):
                first_player.pop()

            for _ in range(len(second_player) - second):
                second_player.pop()

            game += 1
            turn = 0
            first_states = set()
            second_states = set()
            continue

        if winner is None:
            winner = 1 if first > second else 2

        if winner == 1:
            first_player.append(first)
            first_player.append(second)
        else:
            second_player.append(second)
            second_player.append(first)

        winner = None

    return (2, second_player) if len(first_player) == 0 else (1, first_player)


def recursive_play(first_player, second_player):
    queue = deque()
    queue.append(State(1, 0, first_player, second_player, set(), set()))
    winner = None

    while len(queue) > 0:
        state = queue.pop()

        winner, deck = play_recursive_game(winner, state.game, state.round, state.first_deck, state.second_deck, state.first_states, state.second_states, queue)

    return deck


def count_score(deck):
    total = 0
    for i, number in enumerate(deck):
        total += (len(deck) - i) * number
    return total


def deck_snapshot(deck):
    return ",".join(map(str, deck))


def run_lines(lines):
    first_player, second_player = parse_input(lines)

    winner = recursive_play(first_player, second_player)

    return count_score(winner)


def run():
    return run_lines(from_file("inputs/22_crab_game"))


if __name__ == '__main__':
    test_input = ["Player 1:\n", "9\n", "2\n", "6\n", "3\n", "1\n", "\n", "Player 2:\n", "5\n", "8\n", "4\n", "7\n", "10\n", "\n"]

    test(291, run_lines(test_input))
    test(35565, run_lines(from_file("inputs/22_crab_game")), comparator=lambda a, e: a < e)
    print(run())
