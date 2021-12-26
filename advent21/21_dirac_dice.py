from Util import test


class Die:
    def __init__(self):
        self.__side = 0
        self.__rolled = 0

    def roll(self):
        self.__side += 1
        self.__rolled += 1

        if self.__side > 100:
            self.__side = 1

        return self.__side

    def get_rolled(self):
        return self.__rolled

    def __str__(self):
        return "Rolled %d times, face: %d" % (self.__rolled, self.__side)


class Player:
    def __init__(self, starting_position: int, die: Die):
        self.__position = starting_position
        self.__score = 0
        self.__die = die

    def turn(self):
        move = self.__die.roll() + self.__die.roll() + self.__die.roll()

        self.__move(move)
        self.__score += self.__position

        return self.__score >= 1000

    def __move(self, move):
        self.__position += move % 10
        if self.__position > 10:
            self.__position %= 10

    def get_score(self):
        return self.__score

    def __str__(self):
        return "at %d, score: %d" % (self.__position, self.__score)


class ImmutablePlayer:
    def __init__(self, starting_position, score, target):
        self.__position = starting_position
        self.__score = score
        self.__target = target

    def __check_win(self, score):
        return score >= self.__target

    def move(self, move):
        position = self.__position + move % 10
        if position > 10:
            position %= 10

        return ImmutablePlayer(position, self.__score + position, self.__target)

    def is_winner(self):
        return self.__check_win(self.__score)

    def pos(self):
        return self.__position

    def score(self):
        return self.__score

    def __str__(self):
        return "at %d, score: %d" % (self.__position, self.__score)


def run_game(position_1, position_2):
    die = Die()
    player_1 = Player(position_1, die)
    player_2 = Player(position_2, die)

    while True:
        player_1_won = player_1.turn()
        if player_1_won:
            break

        player_2_won = player_2.turn()
        if player_2_won:
            break

    if player_1_won:
        return player_2.get_score() * die.get_rolled()
    else:
        return player_1.get_score() * die.get_rolled()


def dirac_roll():
    for roll_1 in (1, 2, 3):
        for roll_2 in (1, 2, 3):
            for roll_3 in (1, 2, 3):
                yield roll_1 + roll_2 + roll_3


def dirac_game_1(player_1: ImmutablePlayer, player_2: ImmutablePlayer, step, cache):
    key = (player_1.pos(), player_2.pos(), player_1.score(), player_2.score(), step)
    if key in cache:
        return cache[key]

    all_wins_1 = 0
    all_wins_2 = 0

    for roll_1 in dirac_roll():
        next_player1 = player_1.move(roll_1)
        if next_player1.is_winner():
            all_wins_1 += 1
            continue

        for roll_2 in dirac_roll():
            next_player2 = player_2.move(roll_2)
            if next_player2.is_winner():
                all_wins_2 += 1
                continue

            wins_1, wins_2 = dirac_game_1(next_player1, next_player2, step + 1, cache)
            all_wins_1 += wins_1
            all_wins_2 += wins_2

    cache[key] = all_wins_1, all_wins_2

    return all_wins_1, all_wins_2


def run_dirac_game(position_1, position_2, target):
    player1 = ImmutablePlayer(position_1, 0, target)
    player2 = ImmutablePlayer(position_2, 0, target)

    return dirac_game_1(player1, player2, 0, {})


def run():
    return max(run_dirac_game(1, 10, 21))


def main():
    test(739785, run_game(4, 8))
    test(428736, run_game(1, 10))

    test((27, 0), run_dirac_game(4, 8, 1))
    test((183, 156), run_dirac_game(4, 8, 2))
    test((990, 207), run_dirac_game(4, 8, 3))
    test((2930, 971), run_dirac_game(4, 8, 4))
    test((7907, 2728), run_dirac_game(4, 8, 5))
    test((30498, 7203), run_dirac_game(4, 8, 6))
    test((127019, 152976), run_dirac_game(4, 8, 7))
    test((655661, 1048978), run_dirac_game(4, 8, 8))
    test((4008007, 4049420), run_dirac_game(4, 8, 9))
    test((18973591, 12657100), run_dirac_game(4, 8, 10))

    test((444356092776315, 341960390180808), run_dirac_game(4, 8, 21))

    test(57328067654557, run())


if __name__ == '__main__':
    main()