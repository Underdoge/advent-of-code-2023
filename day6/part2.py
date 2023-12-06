""" Day 6, part 2."""
import time
from math import sqrt


def read_race_info(filename: str) -> list:
    """ Read the race info and return it in a dictionary.

    Args:
        filename (str): The file containing the race info.

    Returns:
        list: The race info in a dictionary.
    """
    times = []
    distances = []
    with open(filename) as file:
        times = file.readline().rstrip().split()[1:]
        distances = file.readline().rstrip().split()[1:]
    return [{"time": int("".join(times)), "distance": int("".join(distances))}]


def ways_you_can_win(race_info: dict) -> int:
    """ Calculate solution for -b^2 + time*b -distance = 0
    where b = time the button stays pressed. This formula was obtained from
    "minimum distance to win"/b*(time-b) = 1.

    Args:
        race_info (dict): a dictionary with the race info.

    Returns:
        (int): The difference of the minimum and maximum button press times.
    """
    solutions_for_b = []
    a = -1
    b = race_info["time"]
    c = -race_info["distance"]
    solutions_for_b.append(int((-b-sqrt(pow(b, 2)-4*a*c))/2*a))
    solutions_for_b.append(int((-b+sqrt(pow(b, 2)-4*a*c))/2*a))
    return solutions_for_b[0]-solutions_for_b[1]

def multiply_ways_you_can_win(races_info: list) -> int:
    """ Go through each race's info and calculate the ways you can win and
        multiply them all together.

    Args:
        races_info (list): A list with each race's info.

    Returns:
        int: The product of all number of ways you can win each race.
    """
    product = 1
    for race_info in races_info:
        product *= ways_you_can_win(race_info)
    return product

if __name__ == '__main__':
    tic = time.perf_counter()
    print(multiply_ways_you_can_win(read_race_info("input.txt")))
    toc = time.perf_counter()
    print(f"Took {toc - tic:0.4f} seconds")
