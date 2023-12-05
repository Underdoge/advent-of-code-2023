import time


def location_from_seed(seed_number: int, filename: str) -> int:
    previous_value = seed_number
    next_value = 0
    with open(filename) as file:
        for line in file:
            if line != "\n" and line.split()[0] != "seeds:" and (
                line.split()[1] != "map:"):
                dest_range_start, source_range_start, range_length = (
                    int(line.split()[0]),
                    int(line.split()[1]),
                    int(line.split()[2]))
                if previous_value >= source_range_start and (
                    previous_value < source_range_start+range_length):
                    next_value = previous_value+(
                        dest_range_start-source_range_start)
            elif line != "\n" and line.split()[1] == "map:":
                if next_value != 0:
                    previous_value = next_value
                    next_value = 0
        if next_value != 0:
            return next_value
        else:
            return previous_value

def read_seeds(filename: str) -> list:
    seeds = []
    with open(filename) as file:
        line = file.readline()
        seeds = line.split()[1:]
    return seeds


def smallest_location(filename: str) -> int:
    seeds = read_seeds(filename)
    locations = []
    for seed in seeds:
        locations.append(location_from_seed(int(seed), filename))
    print(locations)
    return min(locations)

if __name__ == '__main__':
    tic = time.perf_counter()
    print(smallest_location("input.txt"))
    toc = time.perf_counter()
    print(f"Took {toc - tic:0.4f} seconds")
