""" Day 5, part 2. """
import concurrent.futures
import operator
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


def read_ranges(filename: str) -> list:
    """ Store ranges in a list.

    Args:
        filename (str): input filename with ranges.

    Returns:
        list: a list containing the ranges.
    """
    ranges = []
    map = []
    with open(filename) as file:
        for line in file:
            if line != "\n" and line.split()[0] != "seeds:" and (
                line.split()[1] != "map:"):
                dest_range_start, source_range_start, range_length = (
                    int(line.split()[0]),
                    int(line.split()[1]),
                    int(line.split()[2]))
                map.append([dest_range_start, source_range_start, range_length])
            elif line != "\n" and line.split()[1] == "map:":
                if len(map) > 0:
                    map = sorted(map, key=operator.itemgetter(1))
                    ranges.append(map)
                    map = []
    map = sorted(map, key=operator.itemgetter(1))
    ranges.append(map)
    return ranges


def location_from_seed(seed_number: int, ranges: list) -> int:
    """ Calculate the location from a seed number.

    Args:
        seed_number (int): The seed number.
        ranges (list): The ranges.

    Returns:
        int: The location.
    """
    current_value = seed_number
    next_value = 0
    for range in ranges:
        for dest_range_start, source_range_start, range_length in range:
            top = source_range_start+range_length
            if current_value >= source_range_start and (
                current_value < top):
                next_value = current_value+(
                    dest_range_start-source_range_start)
        if next_value != 0:
            current_value = next_value
            next_value = 0
    if next_value != 0:
        return seed_number, next_value
    else:
        return seed_number, current_value


def read_seeds(filename: str) -> list:
    """ Store seeds in a list.

    Args:
        filename (str): Input filename containing the seeds.

    Returns:
        list: List with the seeds.
    """
    with open(filename) as file:
        line = file.readline()
        seeds = [int(x) for x in line.split()[1:]]
    return seeds


def test_range(x: int, seeds: list, ranges: list) -> (int, int):
    """ Create threads to test all values between the range in 10k batches.

    Args:
        x (int): The seed index to test.
        seeds (list): A list containing the seeds.
        ranges (list): A list containing the ranges.

    Returns:
        (int, int): A tuple containing the minimum location and the seed that
            originated it.
    """
    locations = {}
    with ThreadPoolExecutor(max_workers=1000) as executor:
        future_location = [executor.submit(
            location_from_seed, seed, ranges) for seed in range(
                seeds[x], seeds[x]+seeds[x+1], 10000)]
        for future in concurrent.futures.as_completed(future_location):
            seed, location = future.result()
            locations[location] = seed
    return min(locations), locations[min(locations)]


def smallest_location(filename: str) -> int:
    """ Get the smallest locations from all seed ranges, then keep trying
        lower seeds for the lowest location.

    Args:
        filename (str): File containing the seeds and ranges.

    Returns:
        int: The smallest location.
    """
    seeds = read_seeds(filename)
    ranges = read_ranges(filename)
    locations = []
    with ProcessPoolExecutor(max_workers=5) as executor:
        future_location = [executor.submit(test_range, x, seeds, ranges) for x in range(len(seeds)) if x%2 ==0]
        for future in concurrent.futures.as_completed(future_location):
            locations.append(future.result())
    location, seed = min(locations)
    seed -= 1
    _, new_location = location_from_seed(seed, ranges)
    while new_location < location:
        _, location = location_from_seed(seed, ranges)
        seed -= 1
        _, new_location = location_from_seed(seed, ranges)
    return location


if __name__ == '__main__':
    tic = time.perf_counter()
    print(smallest_location("input.txt"))
    toc = time.perf_counter()
    print(f"Took {toc - tic:0.4f} seconds")
