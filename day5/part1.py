""" Day 5, part 1."""
import operator
import time


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
    for map in ranges:
        for dest, source, length in map:
            top = source + length
            if current_value >= source and (
                current_value < top):
                next_value = current_value+(
                    dest - source)
                break
        if next_value != 0:
            current_value = next_value
            next_value = 0
    if next_value != 0:
        return next_value
    else:
        return current_value


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
    for seed in seeds:
        locations.append(location_from_seed(seed, ranges))
    return min(locations)


if __name__ == '__main__':
    tic = time.perf_counter()
    print(smallest_location("input.txt"))
    toc = time.perf_counter()
    print(f"Took {toc - tic:0.4f} seconds")
