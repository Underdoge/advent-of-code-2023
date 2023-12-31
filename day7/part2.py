""" Day 7, part 2. """
import time
from functools import cmp_to_key
from itertools import groupby
from operator import countOf

import numpy as np

ALL_CARDS = ['J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']


def read_cards(filename: str) -> list:
    """ Read all card hands and bid and return them in a list.

    Args:
        filename (str): The file containing the hands.

    Returns:
        list: A list of lists containing the hands and bids.
    """
    hands = []
    with open(filename) as file:
        for line in file:
            hand_and_bid = line.split()
            hands.append({"hand": list(hand_and_bid[0]),
                          "bid": int(hand_and_bid[1])})
    return hands


def hand_strength(hand: list) -> int:
    """ Rate hand strenght from five of a kind being the highest (7), to high
        card being the lowest (1). If 'J' is in the hand, upscale the rate
        accordingly.

    Args:
        hand (list): the 5 card hand.

    Returns:
        int: The hand's strenght from 1 to 7.
    """
    unique = np.unique(hand)
    # Five of a kind
    if len(unique) == 1:
        return 7
    # Four of a kind
    elif countOf(hand, hand[0]) == 4 or countOf(hand, hand[1]) == 4:
        if 'J' in unique:
            return 7
        else:
            return 6
    # Full house
    elif len(unique) == 2:
        if 'J' in unique:
            return 7
        else:
            return 5
    # Three of a kind
    elif (countOf(hand, hand[0]) == 3 or (
        countOf(hand, hand[1]) == 3 or countOf(hand, hand[4]) == 3)):
        if 'J' in unique:
            return 6
        else:
            return 4
    # Two pair
    elif len(unique) == 3:
        pairs = 0
        for card in unique:
            if countOf(hand, card) == 2:
                pairs += 1
        if pairs == 2:
            if countOf(hand, 'J') == 1:
                return 5
            elif countOf(hand, 'J') == 2:
                return 6
            else:
                return 3
    # One pair
    elif len(unique) == 4:
        if 'J' in unique:
            return 4
        else:
            return 2
    # High card
    elif 'J' in unique:
        return 2
    else:
        return 1


def compare_hands(hand_1: list, hand_2: list) -> int:
    """ Compare the first card of each hand, if they are the same repeat until
        we reach the last card.

    Args:
        hand_1 (list): The hand to compare.
        hand_2 (list): The hand to compare.

    Returns:
        int: -1 if hand_1 should go first, 1 if after, 0 if they are the same.
    """
    strength = 0
    for idx in range(len(hand_1["hand"])):
        if ALL_CARDS.index(hand_1["hand"][idx]) < ALL_CARDS.index(
            hand_2["hand"][idx]):
            strength = -1
            break
        elif ALL_CARDS.index(hand_1["hand"][idx]) > ALL_CARDS.index(
            hand_2["hand"][idx]):
            strength = 1
            break
    return strength


def sort_hands(hands: list) -> list:
    """ Sort the provided hands list by type, then by card strength.

    Args:
        hands (list): The hands to sort.

    Returns:
        list: The sorted hands list.
    """
    type_groups = []
    sorted_hands = []
    for hand in hands:
        hand["type"] = hand_strength(hand["hand"])
    # Sort by type
    hands = sorted(hands, key=lambda key: key["type"])
    # Group by type
    for _, group in groupby(hands, key=lambda key: key["type"]):
        type_groups.append(list(group))
    # Sort groups by hand strength
    for idx, group in enumerate(type_groups):
        type_groups[idx] = sorted(group, key=cmp_to_key(compare_hands))
    # Create new list with sorted groups
    for group in type_groups:
        for hand in group:
            sorted_hands.append(hand)
    return sorted_hands


def total_winnings(sorted_hands: list) -> int:
    """ Calculate the total winnings by adding all hands' bid multiplied by
        their rank which is the position in the list + 1.

    Args:
        sorted_hands (list): The list of hands sorted by type and card
            strength.

    Returns:
        int: The total sum of winnings.
    """
    winnings = 0
    for idx, hand in enumerate(sorted_hands):
        winnings += (idx+1)*hand["bid"]
    return winnings


if __name__ == '__main__':
    tic = time.perf_counter()
    print(total_winnings(sort_hands(read_cards("input.txt"))))
    toc = time.perf_counter()
    print(f"Took {toc - tic:0.4f} seconds")
