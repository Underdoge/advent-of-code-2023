""" Day 2, part 1."""
import re


def get_cubes(line: str,
              red: int, green: int, blue: int) -> int:
    """ Determine if the provided line contains valid games.

    Args:
        line (str): A string with a list of cubes.
        red (int): The number of red cubes.
        green (int): The number of green cubes.
        blue (int): The number of blue cubes.

    Returns:
        int: The ID of the game if it's valid, otherwise zero.
    """
    invalid_red_cubes = len(list(filter(
        lambda x: x if int(re.search("[0-9]?[0-9]",x)[0]) > red else None,
        re.findall("[0-9]?[0-9]\\sr", line))))
    invalid_green_cubes = len(list(filter(
        lambda x: x if int(re.search("[0-9]?[0-9]",x)[0]) > green else None,
        re.findall("[0-9]?[0-9]\\sg", line))))
    invalid_blue_cubes = len(list(filter(
        lambda x: x if int(re.search("[0-9]?[0-9]",x)[0]) > blue else None,
        re.findall("[0-9]?[0-9]\\sb", line))))
    return int(re.search("[0-9]?[0-9]?[0-9]", line)[0]) if (
        invalid_red_cubes == 0 and invalid_green_cubes == 0
        and invalid_blue_cubes == 0) else 0


if __name__ == '__main__':
    sum_ids = 0
    with open('input.txt') as file:
        for line in file:
            sum_ids += get_cubes(line, red=12, green=13, blue=14)
    print(sum_ids)
