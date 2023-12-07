""" Day 6, part 1."""
import time
from math import ceil, floor, sqrt, modf


def read_race_info(filename: str) -> dict:
    """ Read the race info and return it in a dictionary.

    Args:
        filename (str): The file containing the race info.

    Returns:
        list: The races info each in a dictionary.
    """
    times = []
    distances = []
    races_info = []
    with open(filename) as file:
        times = [int(x) for x in file.readline().rstrip().split()[1:]]
        distances = [int(x) for x in file.readline().rstrip().split()[1:]]
    for idx, time in enumerate(times):
        races_info.append({"time": time, "distance": distances[idx]})
    return races_info


def ways_you_can_win(race_info: dict) -> int:
    """ Calculate solution for -b^2 + time*b - distance = 0
    where b = time the button stays pressed. This formula was obtained from
    "race distance"/b*(time-b) = 1.

    Number of ways you can win are always between (but not inclusive) solutions
    of b, see https://t.ly/FFwnp.

    Args:
        race_info (dict): a dictionary with the race info.

    Returns:
        (int): The difference of the minimum and maximum button press times.
    """
    solutions_for_b = []
    a = -1
    b = race_info["time"]
    c = -race_info["distance"]
    solutions_for_b.append((-b-sqrt(pow(b, 2)-4*a*c))/2*a)
    solutions_for_b.append((-b+sqrt(pow(b, 2)-4*a*c))/2*a)
    solutions_for_b = sorted(solutions_for_b)
    frac_1, _ = modf(solutions_for_b[1])
    if frac_1 == 0:
        solutions_for_b[1] -= 1
        solutions_for_b[0] += 1
    else:
        solutions_for_b[1] = floor(solutions_for_b[1])
        solutions_for_b[0] = ceil(solutions_for_b[0])
    return solutions_for_b[1]-solutions_for_b[0]+1


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
    print("Result:", multiply_ways_you_can_win(read_race_info("input.txt")))
    toc = time.perf_counter()
    print(f"Took {toc - tic:0.4f} seconds")
