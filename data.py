import random
import os
import local
from typing import List


def create_empty_grid(rows: int, cols: int) -> List[List[int]]:
    """
    Creates an empty grid (all cells are dead).

    Args:
        rows (int): number of rows
        cols (int): number of columns

    Returns:
        List[lList[int]]: a list of lists with zeros
    """

    if rows < 1 or cols < 1:
        raise ValueError(f'{local.POSITIVE_SIZES}')

    return [[0] * cols for row_index in range(rows)]


def random_grid(rows: int, cols: int, prob: float = 0.3) -> List[List[int]]:
    """
    Fills the grid with random values with a given probability of life.

    Args:
        rows (int): number of rows
        cols (int): number of cols
        prob (float): probability of a live cell appearing (from 0 to 1)

    Returns:
        List[List[int]]: a grid with random values
    """

    if not 0 <= prob <= 1:
        raise ValueError(f'{local.PROBABILITY}')

    grid_data = []

    for row_index in range(rows):
        row = [1 if random.random() < prob else 0 for col_index in range(cols)]
        grid_data.append(row)
    return grid_data


def load_grid_from_file(filename: str) -> List[List[int]]:
    """
    Reads the grid from a text file.
    File format: each line contains a sequence of 0 and 1 without spaces.
    Example:
    00100
    01110
    00000
    Args:
        filename (str): name of the file

    Returns:
        List[List[int]]: a grid from the file
    """

    if not os.path.exists(filename):
        raise FileNotFoundError(f'{local.FILE} "{filename}" {local.NOT_FOUND}')

    loaded_grid = []

    with open(filename, 'r', encoding='utf-8') as f:
        for line_num, raw_line in enumerate(f, 1):
            processed_line = raw_line.strip()

            if not processed_line:
                continue

            if not all(char in '01' for char in processed_line):
                raise ValueError(f'{local.INVALID_CHARACTERS}')

            loaded_grid.append([int(char) for char in processed_line])

    if not loaded_grid:
        raise ValueError(f'{local.FILE} "{filename}" {local.NOT_CONTAIN_DATA}')

    expected_cols = len(loaded_grid[0])
    for row_idx, row_data in enumerate(loaded_grid):
        if len(row_data) != expected_cols:
            raise ValueError(f'{local.LINE_LENGTH} {row_idx + 1} {local.NOT_MATCH_EXPECTED}')
    return loaded_grid


def save_grid_to_file(grid: List[List[int]], filename: str) -> None:
    """
    Saves the grid to a file.

    Args:
        grid (list): grid to save
        filename (str): name of the file
    """

    if not grid or not grid[0]:
        raise ValueError(f'{local.EMPTY_GRID}')

    first_row = len(grid[0])
    for row_idx, row_data in enumerate(grid):
        if len(row_data) != first_row:
            raise ValueError(f'{local.ERROR_IN_LINE} {row_idx + 1}: {local.DIFFERENT_LENGTHS}')

    with open(filename, 'w', encoding='utf-8') as f:
        for row in grid:
            f.write(''.join(str(cell) for cell in row) + '\n')


def set_cell(grid: List[List[int]], row: int, col: int, value: int) -> bool:
    """
    Sets the state of a specific cell.

    Args:
        grid (List[List[int]]): grid
        row (int): row index
        col (int): column index
        value (int): value (0 or 1)

    Returns:
        True if successful, False if the coordinates are out of range
    """

    if 0 <= row < len(grid) and 0 <= col < len(grid[0]):
        grid[row][col] = value
        return True
    return False
