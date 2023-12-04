from Util import test, from_file


class Card:
    def __init__(self, name, winning_set, current_list):
        self.name = name
        self.winning_set = winning_set
        self.current_list = current_list

    def __str__(self):
        return "Card %d: %s | %s" % (self.name, self.winning_set, self.current_list)


def parse(lines):
    cards = []
    for line in lines:
        line = line.strip()
        name, numbers = line.split(": ")
        name = int(name[4:].strip())

        winning_n, current_n = numbers.split(" | ")

        winning_set = set(map(int, winning_n.split()))
        current_list = list(map(int, current_n.split()))

        cards.append(Card(name, winning_set, current_list))

    return cards


def count_numbers(card):
    matches = 0
    for number in card.current_list:
        if number in card.winning_set:
            if matches == 0:
                matches = 1
            else:
                matches *= 2

    return matches


def count_simple_numbers(card):
    matches = 0
    for number in card.current_list:
        if number in card.winning_set:
            matches += 1

    return matches


def part_1(lines):
    cards = parse(lines)

    total = 0
    for card in cards:
        total += count_numbers(card)
    return total


def part_2(lines):
    cards = parse(lines)
    cards_count = {card.name: 1 for card in cards}

    for card in cards:
        card_count = cards_count.get(card.name, 0)
        matches = count_simple_numbers(card)
        for i in range(matches):
            next_card_name = card.name + i + 1
            existing_card = cards_count.get(next_card_name, 0)
            cards_count[next_card_name] = existing_card + card_count

    return sum(cards_count.values())


def main():
    test(13, part_1(from_file("test_inputs/04_scratch_cards")))
    test(21821, part_1(from_file("inputs/04_scratch_cards")))

    test(30, part_2(from_file("test_inputs/04_scratch_cards")))
    print(part_2(from_file("inputs/04_scratch_cards")))


if __name__ == '__main__':
    main()
