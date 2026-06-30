import sys
from render.ascii import ascii_render
from render.window_render import window_render
from mazegen import Maze
from render.tui_utils import loading

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>")
        sys.exit(1)
    maze = Maze(sys.argv[1])
    loading("Generating maze")
    maze.generate()
    loading("Solving maze")
    maze.solve()
    loading("Saving maze")
    maze.save(maze.grid)
    win = False if maze.render == "ASCII" else True
    if win:
        window_render(maze.output_file, maze.protected)
    else:
        ascii_render(maze.output_file, protected=maze.protected)
