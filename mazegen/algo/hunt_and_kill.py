def init_grid(width: int, height: int) -> tuple[list[bool], list[int]]:
    return (
        [[15 for _ in range(width)] for _ in range(height)],
        [[False for _ in range(width)] for _ in range(height)]
    )


def hunt_and_kill(params: list[int]) -> list[int]:
    print("=== hunt_and_kill ===")
    width, height = params
    grid = []
    visited = []
    grid, visited = init_grid(width, height)
    print(grid)
    print(visited)

