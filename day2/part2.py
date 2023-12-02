""" Day 2, part 2."""
import re


def get_power_of_set(line: str) -> int:
    """ Multiply maximum red, green, and blue cubes.

    Args:
        line (str): A string with a list of cubes.

    Returns:
        int: The maximum of each cube multiplied.
    """
    min_red_cubes = max([int(
        re.search("[0-9]?[0-9]", x)[0]) for x in re.findall("[0-9]?[0-9]\\sr",
                                                            line)])
    min_green_cubes = max([int(
        re.search("[0-9]?[0-9]", x)[0]) for x in re.findall("[0-9]?[0-9]\\sg",
                                                            line)])
    min_blue_cubes = max([int(
        re.search("[0-9]?[0-9]", x)[0]) for x in re.findall("[0-9]?[0-9]\\sb",
                                                            line)])
    return min_red_cubes*min_green_cubes*min_blue_cubes

if __name__ == '__main__':
    sum_powers = 0
    with open('input.txt') as file:
        for line in file:
            sum_powers += get_power_of_set(line)
    print(sum_powers)
