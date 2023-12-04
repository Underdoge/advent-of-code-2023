""" Day 4, part 1."""


def sum_cards(filename: str) -> int:
    """ Count each card's points and return the sum.

    Args:
        filename (str): Name of the input file containing the cards.

    Returns:
        int: The sum of all card points.
    """
    total = 0
    with open(filename) as file:
        for line in file:
            sum = 0
            all_numbers = line.split()
            winning_numbers = all_numbers[2:all_numbers.index("|")]
            numbers_you_have = all_numbers[all_numbers.index("|")+1:]
            for number in numbers_you_have:
                if number in winning_numbers:
                    sum = sum * 2 if sum > 0 else 1
            total += sum
    return total


if __name__ == '__main__':
    print(sum_cards("input.txt"))
