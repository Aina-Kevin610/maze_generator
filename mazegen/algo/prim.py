from __future__ import annotations

import random

from .algo_utils import (
    init_grid,
    remove_wall,
    get_visited_neighbors,
    make_imperfect,
)


def prim(
    width: int,
    height: int,
    protected: set[tuple[int, int]],
    perfect: bool,
    rand: random.Random,
) -> list[list[int]]:
    """
    Generate a maze using Prim's algorithm.

    Starts from a random unprotected cell, then repeatedly picks a random
    cell from the frontier (cells adjacent to the visited region) and
    connects it to a random visited neighbor by removing the shared wall.

    Args:
        width: Number of columns.
        height: Number of rows.
        protected: Set of protected coordinates (pattern cells).
        perfect: If False, randomly remove extra walls after generation.
        rand: Seeded random instance.

    Returns:
        The generated maze grid (integer bit-encoded).
    """
    result = init_grid(width, height)
    grid: list[list[int]] = result[0]
    visited: list[list[bool]] = result[1]

    x = rand.randint(0, width - 1)
    y = rand.randint(0, height - 1)
    while (x, y) in protected:
        x = rand.randint(0, width - 1)
        y = rand.randint(0, height - 1)
    visited[y][x] = True

    in_frontier: set[tuple[int, int]] = set()
    frontier: list[tuple[int, int]] = []

    def expand(cx: int, cy: int) -> None:
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            nx, ny = cx + dx, cy + dy
            if (
                0 <= nx < width
                and 0 <= ny < height
                and not visited[ny][nx]
                and (nx, ny) not in protected
                and (nx, ny) not in in_frontier
            ):
                in_frontier.add((nx, ny))
                frontier.append((nx, ny))

    expand(x, y)

    while frontier:
        idx = rand.randint(0, len(frontier) - 1)
        fx, fy = frontier.pop(idx)
        in_frontier.discard((fx, fy))

        v_nb = get_visited_neighbors(
            visited, width, height, protected, fx, fy
        )
        if v_nb:
            xn, yn = rand.choice(v_nb)
            remove_wall(grid, visited, fx, fy, xn, yn)
            expand(fx, fy)

    if not perfect:
        make_imperfect(grid, width, height, protected, rand)

    return grid
