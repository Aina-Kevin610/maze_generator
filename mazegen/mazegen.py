from .parsing import parse_config


class Maze:
    def __init__(self, filename: str) -> None:
        config = parse_config(filename)
        self.width = config["WIDTH"]
        self.height = config['HEIGHT']
        self.entry = config["ENTRY"]
        self.exit = config["EXIT"]
        self.algo = config["ALGO"]
        self.seed = config["SEED"]

        self.grid = []
        self.visited = []


    def init_grid(self) -> tuple[list[bool], list[int]]:
        self.grid = []

