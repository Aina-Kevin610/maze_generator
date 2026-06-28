import os
import sys
import random
from typing import Any
from render_terminal import print_box


red = "\033[91m"
green = "\033[92m"
yellow = "\033[93m"
bleu = "\033[94m"
magenta = "\033[95m"
cyan = "\033[96m"
reset = "\033[0m"


class ParseError(Exception):
    """
    Exception raised when an invalid configuration format or
    validation error is detected.
    """

    def __init__(self, msg: str = "Invalid config format!") -> None:
        """
        Initialize ParseError.

        Args:
            msg: Error message to display.
        """
        super().__init__(msg)


def read_file(filename: str) -> list[str]:
    """
    Read the configuration file and return its content line by line.

    Args:
        filename: Name of the configuration file.

    Returns:
        A list containing the file lines without newline characters.
    """
    content: list[str] = []
    try:
        with open(filename, "r") as file:
            content = file.read().strip().splitlines()
    except FileNotFoundError:
        print_box(["Error - File not found!", "failure", red])
        sys.exit(1)
    return content


def remove_space(content: list[str]) -> list[str]:
    """
    Remove empty lines from the configuration content.

    Args:
        content: List of file lines.

    Returns:
        A new list without empty lines.
    """
    return [line for line in content if line != ""]


def comment_at_first(content: list[str]) -> list[str]:
    """
    Remove full-line comments from the configuration content.

    A line is considered a comment if it starts with '#'.

    Args:
        content: List of lines to filter.

    Returns:
        A list without comment lines.
    """
    return [line for line in content if not line.startswith("#")]


def comment_at_end(content: list[str]) -> list[list[str]]:
    """
    Remove inline comments from each line.

    Each line is split at the first occurrence of '#'.

    Args:
        content: List of configuration lines.

    Returns:
        A list containing the split parts of each line.
    """
    stripped = [line.strip() for line in content]
    split_lines = [line.split("#", maxsplit=1) for line in stripped]
    return split_lines


def clean_str(content: list[list[str]]) -> list[str]:
    """
    Clean configuration lines after comment removal.

    Only the meaningful part of each line is kept, with
    leading and trailing whitespace removed.

    Args:
        content: List of split lines.

    Returns:
        A list of cleaned configuration strings.
    """
    result: list[str] = []
    for item in content:
        cleaned = item[0].strip()
        result.append(cleaned)
    return result


def test_len_error(content: list[str]) -> list[tuple[str, str]]:
    """
    Validate that each configuration line follows the key=value format.

    Args:
        content: List of configuration lines.

    Returns:
        A list of (key, value) tuples.

    Raises:
        ParseError: If a line does not contain exactly one '='.
    """
    tuples: list[tuple[str, str]] = []
    try:
        for line in content:
            split_line = line.replace(" ", "").split("=")
            if len(split_line) != 2:
                raise ParseError("Invalid config format!")
            tuples.append((split_line[0], split_line[1]))
        return tuples
    except ParseError as error:
        print_box([f"Error - {error}", "failure", red])
        sys.exit(1)


def convert_to_dict(content: list[tuple[str, str]]) -> dict[str, str]:
    """
    Convert a list of key-value tuples into a dictionary.

    Args:
        content: List of (key, value) pairs.

    Returns:
        A dictionary representing the configuration.
    """
    return {key: value.strip() for key, value in content}


def entry_exit(new_content: dict[str, str]) -> dict[str, Any]:
    """
    Convert ENTRY and EXIT values into coordinate tuples.

    Args:
        new_content: Raw configuration dictionary.

    Returns:
        A copy of the configuration dictionary with ENTRY
        and EXIT converted to tuples.
    """
    result: dict[str, Any] = dict(new_content)
    result["ENTRY"] = tuple(new_content["ENTRY"].split(","))
    result["EXIT"] = tuple(new_content["EXIT"].split(","))
    return result


def is_valid(final: dict[Any, Any]) -> None:
    """
    Validate the entire configuration.

    Checks:
        - Required parameters are present.
        - Default values are assigned when needed.
        - Width and height are valid.
        - ENTRY and EXIT coordinates are valid.
        - Algorithm selection is supported.
        - Output filename is valid.
        - PERFECT and SPEED values are valid.

    Args:
        final: Configuration dictionary to validate.

    Raises:
        ParseError: If any configuration value is invalid.
    """
    algos = [
        "DFS",
        "hunt_and_kill",
        "backtracking",
        "prim",
    ]

    mandatory_keys = [
        "HEIGHT",
        "WIDTH",
        "ENTRY",
        "EXIT",
        "PERFECT",
        "OUTPUT_FILE",
    ]

    try:
        for key in mandatory_keys:
            if key not in final:
                raise ParseError(f"Missing mandatory config [{key}]")

        if "ALGO" not in final:
            final["ALGO"] = random.choice(algos)

        if "SEED" not in final:
            final["SEED"] = None

        # FIX: SPEED=None si absent, converti plus bas seulement si présent
        if "SPEED" not in final:
            final["SPEED"] = None

        width = int(final["WIDTH"])
        height = int(final["HEIGHT"])

        entry_x = int(final["ENTRY"][0])
        entry_y = int(final["ENTRY"][1])

        exit_x = int(final["EXIT"][0])
        exit_y = int(final["EXIT"][1])

        if width < 3 or height < 3:
            raise ParseError(
                "Too small HEIGHT or WIDTH (minimum: 3 x 3)!"
            )

        if not final["OUTPUT_FILE"].endswith(".txt"):
            raise ParseError(
                "OUTPUT_FILE extension must be '.txt'!"
            )

        if final["PERFECT"] not in ("True", "False"):
            raise ParseError(
                "PERFECT option must be boolean!"
            )

        if final["ALGO"] not in algos:
            raise ParseError(
                f"Unknown parameter for ALGO! "
                f"Algo must be {algos}"
            )

        # FIX: conversion de SPEED uniquement si la valeur est présente
        if final["SPEED"] is not None:
            speed_int = int(final["SPEED"])
            if speed_int < 1:
                raise ParseError("Invalid SPEED value, must be >= 1")
            final["SPEED"] = speed_int

        if len(final["ENTRY"]) != 2:
            raise ParseError("Invalid ENTRY parameter!")

        if len(final["EXIT"]) != 2:
            raise ParseError("Invalid EXIT parameter!")

        if not (0 <= entry_x < width):
            raise ParseError("Entry point out of range!")

        if not (0 <= entry_y < height):
            raise ParseError("Entry point out of range!")

        if not (0 <= exit_x < width):
            raise ParseError("Exit point out of range!")

        if not (0 <= exit_y < height):
            raise ParseError("Exit point out of range!")

        if final["ENTRY"] == final["EXIT"]:
            raise ParseError(
                "ENTRY and EXIT cannot be at the same position!"
            )

    except (ValueError, ParseError) as error:
        print_box([f"Error - {error}", "failure", red])
        sys.exit(1)


def parse_config(
    filename: str = "config.txt",
) -> dict[str, Any]:
    """
    Load, clean, validate, and return the configuration.

    Processing steps:
        1. Read the file.
        2. Remove empty lines.
        3. Remove comments.
        4. Extract key-value pairs.
        5. Convert data into a dictionary.
        6. Validate all configuration values.

    Args:
        filename: Name of the configuration file.

    Returns:
        A validated configuration dictionary ready for use.
    """
    content = read_file(filename)

    no_space = remove_space(content)
    no_comment_start = comment_at_first(no_space)
    no_comment_end = comment_at_end(no_comment_start)

    cleaned = clean_str(no_comment_end)

    validated = test_len_error(cleaned)

    if len(validated) < 6:
        print_box(["Error - Missing mandatory parameter!", "failure", red])
        sys.exit(1)

    as_dict = convert_to_dict(validated)

    final = entry_exit(as_dict)

    is_valid(final)

    if "PATTERN" not in final:
        final["PATTERN"] = "42"

    return final
