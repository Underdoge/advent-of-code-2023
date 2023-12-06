import threading
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, wait
import operator


# class MyMapping(collections.abc.Mapping):
class SeedLocator:
    def __init__(self, filename):
        self._smallest_location = 100000000000000000000
        self._seeds = self.read_seeds(filename)
        self._ranges = self.read_ranges(filename)

    @property
    def smallest_location(self):
        return self._smallest_location

    @property
    def seeds(self):
        return self._seeds

    @property
    def ranges(self):
        return self._ranges

    @smallest_location.setter
    def smallest_location(self, location):
        if location < self._smallest_location:
            self._smallest_location = location

    def read_ranges(self, filename: str) -> list:
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


    def location_from_seed(self, seed_number: int, ranges: list) -> int:
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
            self.smallest_location = next_value
        else:
            self.smallest_location = current_value

    def read_seeds(self, filename: str) -> list:
        with open(filename) as file:
            line = file.readline()
            seeds = [int(x) for x in line.split()[1:]]
        return seeds

    def test_range(self, x, seeds, ranges):
        print("Seed:", seeds[x], "Target:", seeds[x]+seeds[x+1])
        with ThreadPoolExecutor(max_workers=1000) as executor:
            for seed in range(seeds[x], seeds[x]+seeds[x+1]):
                executor.submit(self.location_from_seed, seed, ranges)
        print("Finished Seed:", seeds[x], "Target:", seeds[x]+seeds[x+1])
        return self.smallest_location


if __name__ == '__main__':
    seed_locator = SeedLocator("input.txt")
    tic = time.perf_counter()
    with ProcessPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(seed_locator.test_range, x, seed_locator.seeds, seed_locator.ranges) for x in range(len(seed_locator.seeds)) if x%2 ==0]
        for future in futures:
            seed_locator.smallest_location = future.result()
    print(seed_locator.smallest_location)
    toc = time.perf_counter()
    print(f"Took {toc - tic:0.4f} seconds")
