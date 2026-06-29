import sys
from render.ascii import ascii_render
from mazegen import Maze

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>")
        sys.exit(1)
    maze = Maze(sys.argv[1])
    maze.generate()
    maze.solve()
    maze.save(maze.grid)
    ascii_render(maze.output_file)