from __future__ import annotations
import random
from .parsing import parse_config
from .algo import hunt_and_kill


class Maze:
    """
    Generate and solve mazes from a configuration file.

    Supported generation algorithms:
        - Hunt and Kill
    """

    def __init__(self, filename: str = "config.txt") -> None:
        """
        Initialize a Maze instance from the configuration file.

        Args:
            filename: Path to the configuration file.
        """
        config = parse_config(filename)

        self.width: int = int(config["WIDTH"])
        self.height: int = int(config["HEIGHT"])
        self.entry: tuple[str, str] = config["ENTRY"]
        self.exit: tuple[str, str] = config["EXIT"]
        self.algo: str = config["ALGO"]
        self.perfect: bool = config["PERFECT"] == "True"
        self.output_file: str = config["OUTPUT_FILE"]
        self.seed: int | None = config["SEED"]
        self.protected: set[tuple[int, int]] = set()

        self.rand: random.Random = random.Random()
        if self.seed is not None:
            self.rand = random.Random(self.seed)

        self.grid: list[list[int]] = []

    def generate(self) -> list[list[int]]:
        """
        Generate the maze using the algorithm defined in config.

        Returns:
            The generated maze grid (integer bit-encoded).
        """
        if self.algo == "hunt_and_kill":
            self.grid = hunt_and_kill(
                width=self.width,
                height=self.height,
                protected=self.protected,
                perfect=self.perfect,
                rand=self.rand,
            )
        return self.grid