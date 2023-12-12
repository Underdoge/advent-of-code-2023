""" Day 8, part 1. """
import re
import time


def read_instructions(filename: str) -> (list, dict):
    """ Read instructions and network, return it both in a tuple.

    Args:
        filename (str): The file containing the instructions and network.

    Returns:
        (list, list): A tuple with a list of instructions translated from L's
            and R's into 0's and 1's, and a network of nodes in a dictionary
            with the form of  {target : [left jump, right jump]} where target,
            left jump and right jump are groups of three uppercase letters.
    """
    instructions = []
    network = {}
    with open(filename) as file:
        instructions = [0 if x == "L" else 1 for x in file.readline().rstrip()]
        file.readline()
        for line in file:
            key, left, right = re.findall("[\\w]{3}", line.rstrip())
            network[key] = [left, right]
    return instructions, network


def count_steps(instructions: list, network: dict) -> int:
    """ Follow the provided instructions through the network and return the
        steps required.

    Args:
        instructions (list): a list of 0's and 1's that indicate which
            side of the node to read.
        network (dict): the network of nodes.

    Returns:
        int: the sum of steps required to reach ZZZ.
    """
    target_node = 'ZZZ'
    instruction_idx = 0
    instruction_num = len(instructions)
    steps = 1
    next_dir = instructions[instruction_idx]
    next_step = network['AAA'][next_dir]
    while next_step != target_node:
        if next_step == target_node and instruction_idx == 0:
            break
        if instruction_idx + 1 == instruction_num:
            instruction_idx = 0
        else:
            instruction_idx += 1
        next_step=network[next_step][instructions[instruction_idx]]
        next_dir=instructions[instruction_idx]
        steps += 1
    return steps


if __name__ == '__main__':
    tic = time.perf_counter()
    instructions, network = read_instructions("input.txt")
    print("Steps:", count_steps(instructions, network))
    toc = time.perf_counter()
    print(f"Took {toc - tic:0.4f} seconds")
