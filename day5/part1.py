import time
import operator


def read_ranges(filename: str) -> list:
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
    with open(filename) as file:
        line = file.readline()
        seeds = [int(x) for x in line.split()[1:]]
    return seeds


def smallest_location(filename: str) -> int:
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
