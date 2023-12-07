from Util import test, from_file


class Hand:
    def __init__(self, hand, bid):
        self.bid = bid
        self.__hand = hand
        self.__cards = self.__parse_card(hand)
        self.__score = self.__type_score()

    @staticmethod
    def __parse_card(hand):
        cards = {}
        for card in hand:
            cards[card] = cards.get(card, 0) + 1
        return cards

    def __type_score(self):
        if self.__is_five_of_a_kind():
            return 6
        if self.__is_four_of_a_kind():
            return 5
        if self.__is_full_house():
            return 4
        if self.__three_of_a_kind():
            return 3
        if self.__two_pairs():
            return 2
        if self.__one_pair():
            return 1
        if self.__high_card():
            return 0

    def __is_five_of_a_kind(self):
        return len(self.__cards) == 1

    def __is_four_of_a_kind(self):
        return len(self.__cards) == 2 and 4 in self.__cards.values()

    def __is_full_house(self):
        return len(self.__cards) == 2 and 3 in self.__cards.values()

    def __three_of_a_kind(self):
        return len(self.__cards) == 3 and 3 in self.__cards.values()

    def __two_pairs(self):
        values = list(sorted(self.__cards.values()))
        return len(self.__cards) == 3 and values == [1, 2, 2]

    def __one_pair(self):
        return len(self.__cards) == 4

    def __high_card(self):
        return len(self.__cards) == 5

    def upscale_hand(self):
        if self.__score == 6:
            return

        jokers = self.__cards.get(0, 0)
        if jokers == 0:
            return

        updated_hands = [self]

        for j in range(jokers):
            next_updated_hands = []
            for updated_hand in updated_hands:
                for r_card in updated_hand.__cards:
                    if r_card == 0:
                        continue

                    joker_pos = updated_hand.__hand.index(0)
                    cards = list(updated_hand.__hand)
                    cards[joker_pos] = r_card

                    next_updated_hands.append(Hand(cards, self.bid))
            updated_hands = next_updated_hands

        best = max(updated_hands)
        self.__score = best.__score

    def __lt__(self, other):
        if self.__score < other.__score:
            return True
        elif self.__score > other.__score:
            return False
        else:
            for i in range(5):
                self_card = self.__hand[i]
                other_card = other.__hand[i]

                if self_card == other_card:
                    continue

                return self_card < other_card

    def __str__(self):
        name = "???"
        if self.__score == 6:
            name = "five of a kind"
        if self.__score == 5:
            name = "four of a kind"
        if self.__score == 4:
            name = "full house"
        if self.__score == 3:
            name = "three of a kind"
        if self.__score == 2:
            name = "two pairs"
        if self.__score == 1:
            name = "one pair"
        if self.__score == 0:
            name = "high card"

        return "%s: %s" % (self.__hand, name)


def replace_with_numbers(hand, is_part_2):
    cards = []
    for card in hand:
        if card == 'T':
            cards.append(10)
        elif card == 'J':
            cards.append(0 if is_part_2 else 11)
        elif card == 'Q':
            cards.append(12)
        elif card == 'K':
            cards.append(13)
        elif card == 'A':
            cards.append(14)
        else:
            cards.append(int(card))
    return cards


def parse(lines, is_part_2):
    hands = []
    for line in lines:
        hand, bid = line.strip().split()
        bid = int(bid)
        hand = replace_with_numbers(hand, is_part_2)

        hands.append(Hand(hand, bid))

    return hands


def calculate_hand(is_part_2, lines):
    hands = parse(lines, is_part_2)
    for hand in hands:
        hand.upscale_hand()

    hands.sort()

    total = 0
    for mult, hand in enumerate(hands):
        total += (mult + 1) * hand.bid

    return total


def run():
    print(calculate_hand(True, from_file("inputs/07_camel_cards")))


def main():
    test(6440, calculate_hand(False, from_file("test_inputs/07_camel_cards")))
    test(247961593, calculate_hand(False, from_file("inputs/07_camel_cards")))

    test(5905, calculate_hand(True, from_file("test_inputs/07_camel_cards")))
    run()


if __name__ == '__main__':
    main()
