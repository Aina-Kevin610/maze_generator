import os
from .tui_utils import loading, print_box, red, cyan

BG_FLOOR = "\033[40m"
BG_ENTRY = "\033[42m"
BG_EXIT = "\033[41m"
BG_PATH = "\033[46m"
BG_PROT = "\033[100m"
RESET = "\033[0m"

WALL_COLORS = {
    "1": "\033[47m",
    "2": "\033[43m",
    "3": "\033[45m",
    "4": "\033[44m",
}

N = 1 << 0
E = 1 << 1
S = 1 << 2
W = 1 << 3

FLOOR = BG_FLOOR + "  " + RESET


def cell_bg(
    x: int,
    y: int,
    entry: tuple[int, int],
    exit_: tuple[int, int],
    path_set: set[tuple[int, int]],
    show_path: bool,
    protected: set[tuple[int, int]] | None = None,
) -> str:
    if (x, y) == entry:
        return BG_ENTRY + "  " + RESET
    if (x, y) == exit_:
        return BG_EXIT + "  " + RESET
    if show_path and (x, y) in path_set:
        return BG_PATH + "  " + RESET
    if protected and (x, y) in protected:
        return BG_PROT + "  " + RESET
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
    wall_color: str,
    show_path: bool,
    protected: set[tuple[int, int]] | None = None,
) -> None:
    height = len(grid)
    width = len(grid[0])
    path_set = set(path)
    wall_str = wall_color + "  " + RESET

    for y in range(height):
        top = ""
        mid = ""
        for x in range(width):
            cell = grid[y][x]
            top += wall_str
            top += wall_str if cell & N else FLOOR
            mid += wall_str if cell & W else FLOOR
            mid += cell_bg(x, y, entry, exit_, path_set, show_path, protected)
        top += wall_str
        mid += wall_str
        print(top)
        print(mid)

    print(wall_str * (width * 2 + 1))


def ascii_render(
    filename: str = "maze.txt",
    protected: set[tuple[int, int]] | None = None,
    info: list[str] | None = None,
) -> None:

    show_path = True
    current_wall_key = "1"

    while True:
        os.system("cls" if os.name == "nt" else "clear")

        try:
            grid, entry, exit_, path = parse(filename)
        except FileNotFoundError:
            print_box((f"Can't find '{filename}'.", "Error", red))
            return

        wall_color = WALL_COLORS[current_wall_key]

        legend = (
            f"\n  {BG_ENTRY}  {RESET} entry   "
            f"{BG_EXIT}  {RESET} exit   "
            f"{BG_PATH}  {RESET} path (Visible: {show_path})   "
            f"{BG_PROT}  {RESET} protected\n"
        )
        loading("generating...")

        if info:
            print_box((info, "Info", cyan))
        print(legend)

        render(
            grid, entry, exit_,
            path, wall_color, show_path,
            protected=protected or set()
        )

        print("\n=== Menu ===")
        print("[R] Regenerate")
        print("[H] show\\hide path")
        print("[C] Change wall color")
        print("[Q] exit")

        choice = input("\nYour choice : ").strip().upper()

        if choice == "Q":
            print("See you evaluator !")
            break
        elif choice == "H":
            show_path = not show_path
        elif choice == "C":
            print("\nAvalable color:")
            print("1: White | 2: Yellow | 3: Magenta | 4: Blue")
            c_choice = input("Choose a number : ").strip()
            if c_choice in WALL_COLORS:
                current_wall_key = c_choice
        elif choice == "R":
            print("\nRegenerating...")
            if os.path.exists("a_maze_ing.py"):
                os.system("python3 a_maze_ing.py config.txt")
            else:
                pass
