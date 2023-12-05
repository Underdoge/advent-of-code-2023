import time


def read_ranges(filename: str) -> list:
    ranges = []
    range = []
    with open(filename) as file:
        for line in file:
            if line != "\n" and line.split()[0] != "seeds:" and (
                line.split()[1] != "map:"):
                dest_range_start, source_range_start, range_length = (
                    int(line.split()[0]),
                    int(line.split()[1]),
                    int(line.split()[2]))
                range.append([dest_range_start, source_range_start, range_length])
            elif line != "\n" and line.split()[1] == "map:":
                if len(range) > 0:
                    ranges.append(range)
                    range = []
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
    seeds = []
    with open(filename) as file:
        line = file.readline()
        seeds = line.split()[1:]
    return seeds


def smallest_location(filename: str) -> int:
    seeds = read_seeds(filename)
    ranges = read_ranges(filename)
    last_smallest_location = 10000000
    x=0
    while x+1 <= len(seeds):
        print("Seed:", int(seeds[x]), "Target:", int(seeds[x])+int(seeds[x+1]))
        for seed in range(int(seeds[x]), int(seeds[x])+int(seeds[x+1]), 1):
            new_loc = location_from_seed(int(seed), ranges)
            if new_loc < last_smallest_location:
                last_smallest_location = new_loc
        x += 2
    return last_smallest_location


if __name__ == '__main__':
    tic = time.perf_counter()
    print(smallest_location("input.txt"))
    toc = time.perf_counter()
    print(f"Took {toc - tic:0.4f} seconds")
