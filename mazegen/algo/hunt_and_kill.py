from __future__ import annotations
import random
from .algo_utils import (
    init_grid,
    remove_wall,
    get_neighbors,
    get_visited_neighbors,
    make_imperfect,
)


def hunt_and_kill(
    width: int,
    height: int,
    protected: set[tuple[int, int]],
    perfect: bool,
    rand: random.Random,
) -> list[list[int]]:
    """
    Generate a maze using the Hunt and Kill algorithm.

    Args:
        width: Number of columns.
        height: Number of rows.
        protected: Set of protected coordinates (pattern cells).
        perfect: If False, randomly remove extra walls after generation.
        rand: Seeded random instance.

    Returns:
        The generated maze grid (integer bit-encoded).
    """
    grid, visited = init_grid(width, height)

    # Pick a random unprotected starting cell
    x = rand.randint(0, width - 1)
    y = rand.randint(0, height - 1)
    while (x, y) in protected:
        x = rand.randint(0, width - 1)
        y = rand.randint(0, height - 1)
    visited[y][x] = True

    phase = "kill"
    current_x, current_y = x, y

    while phase != "done":
        if phase == "kill":
            neighbors = get_neighbors(
                visited, width, height, protected, current_x, current_y
            )
            if neighbors:
                xn, yn = rand.choice(neighbors)
                current_x, current_y, _ = remove_wall(
                    grid, visited, current_x, current_y, xn, yn
                )
            else:
                phase = "hunt"

        elif phase == "hunt":
            found: tuple[int, int] | None = None
            for i in range(height):
                for j in range(width):
                    if not visited[i][j] and (j, i) not in protected:
                        v_nb = get_visited_neighbors(
                            visited, width, height, protected, j, i
                        )
                        if v_nb:
                            xn, yn = rand.choice(v_nb)
                            remove_wall(grid, visited, j, i, xn, yn)
                            found = (j, i)
                            break
                if found:
                    break
            if found is None:
                phase = "done"
            else:
                current_x, current_y = found
                phase = "kill"

    if not perfect:
        make_imperfect(grid, width, height, protected, rand)

    return grid
