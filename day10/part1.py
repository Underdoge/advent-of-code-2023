""" Day 10, part 1."""
import sys
import time


def read_pipes(filename: str) -> list:
    """ Read pipes from file and return them in a list of lists.

    Args:
        filename (str): The file containing the pipe values.

    Returns:
        list: A list of lists with all the pipes.
    """
    pipes = []
    with open(filename) as file:
        for line in file:
            pipes.append(list(line.rstrip()))
    return pipes

def find_start(pipes: list) -> (int, int):
    """ Find the "S" pipe and return its position.

    Args:
        pipes (list): A list of lists with all the pipes.

    Returns:
        (int, int): The y, x position of the 'S' pipe.
    """
    for idx_y, pipe_line in enumerate(pipes):
        if 'S' in pipe_line:
            return idx_y, pipe_line.index('S')


def count_steps(pipes: list, start: (int, int)) -> int:
    """ Return the steps required to fill the loop from the start.

    Args:
        pipes (list): A list of lists with all the pipes.
        start (int, int): The starting point.

    Returns:
        int: The amount of steps to return to the start.
    """
    height = len(pipes)
    width = len(pipes[0])
    steps = 0
    def flood_fill_pipes(pipes: list, x: int, y: int, dir: str,
                         start: (int, int), steps: int) -> int:
        """ Recursively follow the pipes and return the steps required to
        fill the loop from the start.

        Args:
            pipes (list): A list of lists with all the pipes.
            x (int): The current position's x.
            y (int): The current position's y.
            dir (str): Previous call's direction.
            start (int, int): The starting point.
            steps (int): The number of steps at this position.

        Returns:
            int: The amount of steps to return to the start.
        """
        if x == start[1] and y == start[0]:
            return steps
        else:
            match dir:
                case 'up':
                    if pipes[y][x] == '|':
                        return flood_fill_pipes(pipes, x, y-1,
                                                'up', start, steps+1)
                    elif pipes[y][x] == 'F':
                        return flood_fill_pipes(pipes, x+1, y,
                                                'right', start, steps+1)
                    elif pipes[y][x] == '7':
                        return flood_fill_pipes(pipes, x-1, y,
                                                'left', start, steps+1)
                case 'down':
                    if pipes[y][x] == '|':
                        return flood_fill_pipes(pipes, x, y+1,
                                                'down', start, steps+1)
                    elif pipes[y][x] == 'L':
                        return flood_fill_pipes(pipes, x+1, y,
                                                'right', start, steps+1)
                    elif pipes[y][x] == 'J':
                        return flood_fill_pipes(pipes, x-1, y,
                                                'left', start, steps+1)
                case 'left':
                    if pipes[y][x] == '-':
                        return flood_fill_pipes(pipes, x-1, y,
                                                'left', start, steps+1)
                    elif pipes[y][x] == 'F':
                        return flood_fill_pipes(pipes, x, y+1,
                                                'down', start, steps+1)
                    elif pipes[y][x] == 'L':
                        return flood_fill_pipes(pipes, x, y-1,
                                                'up', start, steps+1)
                case 'right':
                    if pipes[y][x] == '-':
                        return flood_fill_pipes(pipes, x+1, y,
                                                'right', start, steps+1)
                    elif pipes[y][x] == 'J':
                        return flood_fill_pipes(pipes, x, y-1,
                                                'up', start, steps+1)
                    elif pipes[y][x] == '7':
                        return flood_fill_pipes(pipes, x, y+1,
                                                'down', start, steps+1)


    y, x = start
    if y-1 >= 0 and pipes[y-1][x] in ['|', 'F', '7']:
        steps = flood_fill_pipes(pipes, x, y-1, 'up', start, 1)
    elif y+1 <= height-1 and pipes[y+1][x] in ['|', 'L', 'J']:
        steps = flood_fill_pipes(pipes, x, y+1, 'down', start, 1)
    elif x-1 >= 0 and pipes[y][x-1] in ['-', 'F', 'L']:
        steps = flood_fill_pipes(pipes, x-1, y, 'left', start, 1)
    elif x+1 <= width-1 and pipes[y][x+1] in ['-', 'J', '7']:
        steps = flood_fill_pipes(pipes, x+1, y, 'right', start, 1)
    return steps


if __name__ == '__main__':
    sys.setrecursionlimit(100000000)
    tic = time.perf_counter()
    pipes = read_pipes("input.txt")
    start = find_start(pipes)
    print("Number of steps:", int(count_steps(pipes, start)/2))
    toc = time.perf_counter()
    print(f"Took {toc - tic:0.4f} seconds")
