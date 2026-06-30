import sys
import time
from typing import Any


red = "\033[91m"
green = "\033[92m"
yellow = "\033[93m"
bleu = "\033[94m"
magenta = "\033[95m"
cyan = "\033[96m"
reset = "\033[0m"


colors = [
    0xFFFFFFFF,
    0xFF0000FF,
    0x00FF00FF,
    0x0000FFFF,
    0xFFFF00FF,
    0x00FFFFFF,
    0xFF00FFFF,
    0x8B0000FF,
    0xDC143CFF,
    0xB22222FF,
]


def box(msg: str | list[str], label: str, color: str) -> None:
    """
    Print a decorated terminal box around a message.

    Args:
        msg: Message string or list of strings to display.
        label: Label shown in the box header.
        color: ANSI color code applied to the box borders.
    """
    prefix = "┏━━━━━━━━━━>>>"
    suffix = "<<<━━━━━━━━━━"

    if isinstance(msg, str):
        msgs = [msg]
    else:
        msgs = [str(m) for m in msg]

    min_w_header = len(prefix) + len(label) + len(suffix) + 1
    min_w_msg = max((len(m) + 6 for m in msgs), default=0)
    w = max(min_w_header, min_w_msg)

    dashes = "━" * (w - len(prefix) - len(label) - len(suffix) - 1)
    header = f"{prefix}{label}{suffix}{dashes}┓"

    lines = [f"{color}{header}{reset}"]
    for m in msgs:
        lines.append(f"{color}┃{reset}  {m:<{w - 6}}  {color}┃{reset}")
    lines.append(f"{color}┗{'━' * (w - 2)}┛{reset}")

    print("\n".join(lines))


def print_box(param: Any) -> None:
    """
    Unpack a parameter tuple and call box().

    Args:
        param: A tuple of (message, label, color).
    """
    mess, label, color = param
    box(mess, label, color)


def loading(mess: str, sec: float = 0.1) -> None:
    """
    Display an animated loading spinner in the terminal.

    The animation runs for approximately two seconds and shows
    a rotating spinner alongside a status message.

    Args:
        mess: Message displayed during loading.
        sec: Delay between animation frames.
    """
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end = time.time() + 2
    while time.time() < end:
        for f in frames:
            sys.stdout.write(f"\r{cyan}{f}{reset} {mess}...")
            sys.stdout.flush()
            time.sleep(sec)
    sys.stdout.write(f"\r{cyan}✓{reset} Done!              \n")
