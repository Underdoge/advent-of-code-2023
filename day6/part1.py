""" Day 6, part 1."""
import time


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
    """ Calculate the number of ways you can win a race.

    Args:
        race_info (dict): Contains the race time and distance.

    Returns:
        int: The number of ways you can win.
    """
    wins = 0
    for button_press in range(race_info["distance"]):
        if button_press*(race_info["time"]-button_press) > (
            race_info["distance"]):
            wins += 1
    return wins

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
