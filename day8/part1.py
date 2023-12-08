""" Day 8, part 1. """


def read_instructions(filename: str) -> (list, list):
    """ Read instructions and network, return it both in a tuple.

    Args:
        filename (str): The file containing the instructions and network.

    Returns:
        (list, list): A tuple with the instructions and network.
    """
    instructions = []
    network = []
    with open(filename) as file:
        instructions = file.readline().rsplit()
        file.readline()
        for line in file:
            network.append(line)
    return instructions, network

print(read_instructions("test.txt"))
