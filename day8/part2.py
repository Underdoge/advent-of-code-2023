""" Day 8, part 2. """
import math
import operator
import re
import time
from functools import reduce


def read_instructions(filename: str) -> (list, dict):
    """ Read instructions and network, return it both in a tuple.

    Args:
        filename (str): The file containing the instructions and network.

    Returns:
        (list, dict): A tuple with a list of instructions translated from L's
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


def is_prime(number: int) -> bool:
    """ Check if a provided number is prime.

    Args:
        number (int): The number to check.

    Returns:
        bool: True if it's prime, False otherwise.
    """
    return all(number % x != 0 for x in range(2, int(math.sqrt(number)) + 1))


def distances_between_z(instructions: list, network: dict) -> list:
    """ Follow the provided instructions through the network and return the
        steps required for each sequence to reach a 'Z' element.

    Args:
        instructions (list): a list of 0's and 1's that indicate which
            side of the node to read.
        network (dict): the network of nodes.

    Returns:
        list: the number of steps required to reach a 'Z' element for each
            sequence.
    """
    current_nodes = [x for x in network if x[2] == "A"]
    instruction_idx = 0
    instruction_num = len(instructions)
    steps = 0
    current_nodes_last_chars = [x[2] for x in current_nodes]
    node_num = len(current_nodes)
    steps_between_z = [0 for x in range(node_num)]
    while operator.countOf(current_nodes_last_chars, 'Z') != node_num:
        if (operator.countOf(current_nodes_last_chars, 'Z') == 1):
            steps_between_z[current_nodes_last_chars.index('Z')] = steps
        if operator.countOf(steps_between_z, 0) == 0:
            # Found all distances between Z's.
            break
        new_steps = []
        new_dirs = []
        for node in current_nodes:
            new_steps.append(network[node][instructions[instruction_idx]])
            new_dirs.append(instructions[instruction_idx])
        if instruction_idx + 1 == instruction_num:
            instruction_idx = 0
        else:
            instruction_idx += 1
        current_nodes = new_steps
        current_nodes_last_chars = [x[2] for x in current_nodes]
        steps += 1
    return steps_between_z


def product_of_lowest_common_prime_factors(steps_between_z: list) -> int:
    """ Multiply the lowest common prime factors of the number of steps between
    Z'z of each sequence, not including 1 and the the number of steps.
    See https://www.youtube.com/watch?v=O6DNWMxG_tk.

    Args:
        steps_between_z (list): Number of steps between Z's of each sequence.

    Returns:
        int: The product of the multiplication.
    """
    product = 1
    used_factors = []
    factors_per_sequence = [0 for x in range(len(steps_between_z))]
    for idx, steps in enumerate(steps_between_z):
        factors_per_sequence[idx] = list(reduce(list.__add__,
                ([i, steps//i] for i in range(
                    1, int(steps**0.5) + 1) if steps % i == 0)))
    for factors in factors_per_sequence:
        for factor in factors:
            if factor not in used_factors and is_prime(factor):
                product *= factor
                used_factors.append(factor)
    return product


if __name__ == '__main__':
    instructions, network = read_instructions("input.txt")
    tic = time.perf_counter()
    distances = distances_between_z(instructions, network)
    print("Steps:", product_of_lowest_common_prime_factors(distances))
    toc = time.perf_counter()
    print(f"Took {toc - tic:0.4f} seconds")
