import sys

BG_WALL = "\033[47m"
BG_FLOOR = "\033[40m"
BG_ENTRY = "\033[42m"
BG_EXIT = "\033[41m"
BG_PATH = "\033[46m"
RESET = "\033[0m"

N = 1 << 0
E = 1 << 1
S = 1 << 2
W = 1 << 3

WALL = BG_WALL + "  " + RESET
FLOOR = BG_FLOOR + "  " + RESET


def cell_bg(
    x: int,
    y: int,
    entry: tuple[int, int],
    exit_: tuple[int, int],
    path_set: set[tuple[int, int]],
) -> str:
    if (x, y) == entry:
        return BG_ENTRY + "  " + RESET
    if (x, y) == exit_:
        return BG_EXIT + "  " + RESET
    if (x, y) in path_set:
        return BG_PATH + "  " + RESET
    return FLOOR


def parse(filename: str) -> tuple[
    list[list[int]],
    tuple[int, int],
    tuple[int, int],
    list[tuple[int, int]],
]:
    with open(filename) as f:
        lines = f.read().splitlines()

    grid_lines: list[str] = []
    rest: list[str] = []
    sep = None
    for line in lines:
        if line == "" and sep is None:
            sep = 0
        elif sep is None:
            grid_lines.append(line)
        elif line:
            rest.append(line)

    grid = [[int(c, 16) for c in row] for row in grid_lines]

    ex, ey = map(int, rest[0].split(","))
    xx, xy = map(int, rest[1].split(","))

    path: list[tuple[int, int]] = []
    if len(rest) >= 3:
        x, y = ex, ey
        for ch in rest[2]:
            path.append((x, y))
            if ch == "N":
                y -= 1
            elif ch == "S":
                y += 1
            elif ch == "E":
                x += 1
            elif ch == "W":
                x -= 1
        path.append((x, y))

    return grid, (ex, ey), (xx, xy), path


def render(
    grid: list[list[int]],
    entry: tuple[int, int],
    exit_: tuple[int, int],
    path: list[tuple[int, int]],
) -> None:
    height = len(grid)
    width = len(grid[0])
    path_set = set(path)

    for y in range(height):
        top = ""
        mid = ""
        for x in range(width):
            cell = grid[y][x]
            top += WALL
            top += WALL if cell & N else FLOOR
            mid += WALL if cell & W else FLOOR
            mid += cell_bg(x, y, entry, exit_, path_set)
        top += WALL
        mid += WALL
        print(top)
        print(mid)

    print(WALL * (width * 2 + 1))


def main() -> None:
    filename = sys.argv[1] if len(sys.argv) > 1 else "maze.txt"
    grid, entry, exit_, path = parse(filename)
    legend = (
        f"\n  {BG_ENTRY}  {RESET} entry   "
        f"{BG_EXIT}  {RESET} exit   "
        f"{BG_PATH}  {RESET} path\n"
    )
    print(legend)
    render(grid, entry, exit_, path)


main()