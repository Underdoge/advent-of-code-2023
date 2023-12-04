""" Day 4, part 2."""


def read_cards(filename: str) -> list:
    """ Read all cards and append them into a list.

    Args:
        filename (str): Name of the input file containing the cards.

    Returns:
        list: a list with all the cards.
    """
    cards = []
    with open(filename) as file:
        for line in file:
            all_numbers = line.split()
            all_numbers[1] = all_numbers[1].replace(":","")
            cards.append(all_numbers)
    return cards

def count_cards(cards: list) -> int:
    """ Get the points of each game and count all the new games cards.

    Args:
        cards (list): A list with all the cards.

    Returns:
        int: The total number of scratchcards.
    """
    new_cards = []
    total_cards = cards
    for card_num in range(len(cards)):
        sum = 0
        winning_numbers = cards[card_num][2:cards[card_num].index("|")]
        numbers_you_have = cards[card_num][cards[card_num].index("|")+1:]
        for number in numbers_you_have:
            if number in winning_numbers:
                sum += 1
        for x in range(sum):
            new_cards.append(cards[int(cards[card_num][1])+x])
    appended_cards = True
    for card in new_cards:
        total_cards.append(card)
    while appended_cards:
        appended_cards = False
        current_cards = []
        for card_num in range(len(new_cards)):
            sum = 0
            winning_numbers = new_cards[card_num][2:new_cards[card_num].index("|")]
            numbers_you_have = new_cards[card_num][new_cards[card_num].index("|")+1:]
            for number in numbers_you_have:
                if number in winning_numbers:
                    appended_cards = True
                    sum += 1
            for x in range(sum):
                current_cards.append(cards[int(new_cards[card_num][1])+x])
        for card in current_cards:
            total_cards.append(card)
        new_cards = current_cards
    return len(total_cards)

if __name__ == '__main__':
    print(count_cards(read_cards("input.txt")))
