""" Day 6, part 2."""
import time
from math import ceil, floor, modf, sqrt


def read_race_info(filename: str) -> dict:
    """ Read the race info and return it in a dictionary.

    Args:
        filename (str): The file containing the race info.

    Returns:
        dict: The race info in a dictionary.
    """
    times = []
    distances = []
    with open(filename) as file:
        times = file.readline().rstrip().split()[1:]
        distances = file.readline().rstrip().split()[1:]
    return {"time": int("".join(times)), "distance": int("".join(distances))}


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


if __name__ == '__main__':
    tic = time.perf_counter()
    print("Result:", ways_you_can_win(read_race_info("input.txt")))
    toc = time.perf_counter()
    print(f"Took {toc - tic:0.4f} seconds")
