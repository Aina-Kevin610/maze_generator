from typing import Optional
import random


def init_grid(
    width: int, height: int
) -> tuple[list[list[int]], list[list[bool]]]:
    """
    Initialize the maze grid and visited matrix.

    Args:
        width: Number of columns.
        height: Number of rows.

    Returns:
        A tuple (grid, visited) where grid is filled with 15 (all walls)
        and visited is filled with False.
    """
    grid: list[list[int]] = [
        [15 for _ in range(width)] for _ in range(height)
    ]
    visited: list[list[bool]] = [
        [False for _ in range(width)] for _ in range(height)
    ]
    return grid, visited


def remove_wall(
    grid: list[list[int]],
    visited: list[list[bool]],
    x: int,
    y: int,
    xn: int,
    yn: int,
) -> tuple[int, int, int]:
    """
    Remove the wall between two adjacent cells.

    Args:
        grid: Maze grid.
        visited: Visited matrix.
        x: X coordinate of current cell.
        y: Y coordinate of current cell.
        xn: X coordinate of neighbor cell.
        yn: Y coordinate of neighbor cell.

    Returns:
        Tuple (xn, yn, opposite_wall_bit).
    """
    dx, dy = xn - x, yn - y
    if dx == 1:
        direction, opposite = 0b0100, 0b0001
    elif dx == -1:
        direction, opposite = 0b0001, 0b0100
    elif dy == 1:
        direction, opposite = 0b0010, 0b1000
    elif dy == -1:
        direction, opposite = 0b1000, 0b0010
    else:
        return xn, yn, 0
    grid[y][x] &= ~direction
    grid[yn][xn] &= ~opposite
    visited[y][x] = True
    visited[yn][xn] = True
    return xn, yn, opposite


def get_neighbors(
    visited: list[list[bool]],
    width: int,
    height: int,
    protected: set[tuple[int, int]],
    x: int,
    y: int,
) -> list[tuple[int, int]]:
    """
    Get unvisited, unprotected neighbors of a cell.

    Args:
        visited: Visited matrix.
        width: Grid width.
        height: Grid height.
        protected: Set of protected coordinates.
        x: X coordinate.
        y: Y coordinate.

    Returns:
        List of valid neighbor coordinates.
    """
    neighbors: list[tuple[int, int]] = []
    for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
        xn, yn = x + dx, y + dy
        if (
            0 <= xn < width
            and 0 <= yn < height
            and not visited[yn][xn]
            and (xn, yn) not in protected
        ):
            neighbors.append((xn, yn))
    return neighbors


def get_visited_neighbors(
    visited: list[list[bool]],
    width: int,
    height: int,
    protected: set[tuple[int, int]],
    x: int,
    y: int,
) -> list[tuple[int, int]]:
    """
    Get visited, unprotected neighbors of a cell.

    Args:
        visited: Visited matrix.
        width: Grid width.
        height: Grid height.
        protected: Set of protected coordinates.
        x: X coordinate.
        y: Y coordinate.

    Returns:
        List of visited neighbor coordinates.
    """
    neighbors: list[tuple[int, int]] = []
    for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
        xn, yn = x + dx, y + dy
        if (
            0 <= xn < width
            and 0 <= yn < height
            and visited[yn][xn]
            and (xn, yn) not in protected
        ):
            neighbors.append((xn, yn))
    return neighbors


def make_imperfect(
    grid: list[list[int]],
    width: int,
    height: int,
    protected: set[tuple[int, int]],
    rand: random.Random,
    rate: float = 0.15,
) -> None:
    """
    Randomly remove walls to create an imperfect maze.

    Args:
        grid: Maze grid.
        width: Grid width.
        height: Grid height.
        protected: Set of protected coordinates.
        rand: Random instance.
        rate: Probability of removing a wall.
    """
    for y in range(height):
        for x in range(width):
            if (x, y) in protected:
                continue
            if x + 1 < width and (x + 1, y) not in protected:
                if rand.random() < rate:
                    grid[y][x] &= ~(1 << 2)
                    grid[y][x + 1] &= ~(1 << 0)
            if y + 1 < height and (x, y + 1) not in protected:
                if rand.random() < rate:
                    grid[y][x] &= ~(1 << 1)
                    grid[y + 1][x] &= ~(1 << 3)