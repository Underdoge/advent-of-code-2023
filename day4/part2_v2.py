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

def count_new_cards(cards: list, new_cards: list, card_gen: dict) -> int:
    """ Count new generated cards recursively.

    Args:
        cards (list): The original cards.
        new_cards (list): The generated cards from the original ones.
        card_gen (dict): A map with original card -> generated cards.

    Returns:
        int: Count of generated new cards.
    """
    total_cards = 0
    appended_cards = False
    current_cards = []
    for card_num in range(len(new_cards)):
        if len(card_gen[int(new_cards[card_num][1])]) > 0:
            appended_cards = True
            for card in card_gen[int(new_cards[card_num][1])]:
                current_cards.append(cards[card-1])
    total_cards += len(current_cards)
    new_cards = current_cards
    if appended_cards:
        return total_cards+count_new_cards(cards, new_cards, card_gen)
    else:
        return total_cards

def count_cards(cards: list) -> int:
    """ Get the points of each game and count all the new games cards.

    Args:
        cards (list): A list with all the cards.

    Returns:
        int: The total number of scratchcards.
    """
    card_generation = {}
    new_cards = []
    total_cards = len(cards)
    for card_num in range(len(cards)):
        sum = 0
        card_generation[card_num+1] = []
        winning_numbers = cards[card_num][2:cards[card_num].index("|")]
        numbers_you_have = cards[card_num][cards[card_num].index("|")+1:]
        for number in numbers_you_have:
            if number in winning_numbers:
                sum += 1
                card_generation[card_num+1].append(card_num+1+sum)
        for x in range(sum):
            new_cards.append(cards[int(cards[card_num][1])+x])
    total_cards += len(new_cards)
    total_cards += count_new_cards(cards, new_cards, card_generation)
    return total_cards

if __name__ == '__main__':
    print(count_cards(read_cards("input.txt")))
