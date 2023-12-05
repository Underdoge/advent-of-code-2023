import concurrent.futures
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


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
                    ranges.append(map)
                    map = []
    ranges.append(map)
    return ranges


def location_from_seed(seed_number: int, ranges: list) -> int:
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
        return next_value
    else:
        return current_value

def read_seeds(filename: str) -> list:
    with open(filename) as file:
        line = file.readline()
        seeds = [int(x) for x in line.split()[1:]]
    return seeds

def test_range(x, seeds, ranges):
    smallest_location = location_from_seed(seeds[0], ranges)
    print("Seed:", seeds[x], "Target:", seeds[x]+seeds[x+1])
    with ThreadPoolExecutor(max_workers=1000) as executor:
        future_location = [executor.submit(location_from_seed, seed, ranges) for seed in range(seeds[x], seeds[x]+seeds[x+1])]
        for future in concurrent.futures.as_completed(future_location):
            location = future.result()
            if location < smallest_location:
                smallest_location = location
    return smallest_location

def smallest_location(filename: str) -> int:
    seeds = read_seeds(filename)
    ranges = read_ranges(filename)
    locations = []
    with ProcessPoolExecutor(max_workers=10) as executor:
        future_location = [executor.submit(test_range, x, seeds, ranges) for x in range(len(seeds)) if x%2 ==0]
        for future in concurrent.futures.as_completed(future_location):
            locations.append(future.result())
    return min(locations)


if __name__ == '__main__':
    tic = time.perf_counter()
    print(smallest_location("input.txt"))
    toc = time.perf_counter()
    print(f"Took {toc - tic:0.4f} seconds")
