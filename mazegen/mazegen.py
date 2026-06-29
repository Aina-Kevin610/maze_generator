from .parsing import parse_config
from .algo import *


class Maze:
    def __init__(self, filename: str) -> None:
        config = parse_config(filename)
        self.width = int(config["WIDTH"])
        self.height = int(config['HEIGHT'])
        self.entry = config["ENTRY"]
        self.exit = config["EXIT"]
        self.algo = config["ALGO"]
        self.seed = config["SEED"]

    
    def generate(self) -> None:
        if self.algo == 'hunt_and_kill':
            hunt_and_kill([self.width, self.height])




