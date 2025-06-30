# quieteye/utils/terminal.py
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.live import Live
from rich.table import Table
from rich.text import Text
from rich.console import Group

import time
import pyfiglet

console = Console()
stop_display = False
_last_update_time = time.time()
_frame_data = {
    "frame": 0,
    "gaze": "N/A",
    "pitch": 0.0,
    "yaw": 0.0,
    "head_status": "N/A",
    "attention_score": 0.0,
}


def update_terminal_data(frame, gaze, pitch, yaw, head_status, score):
    global _frame_data
    _frame_data.update(
        {
            "frame": frame,
            "gaze": gaze,
            "pitch": pitch,
            "yaw": yaw,
            "head_status": head_status,
            "attention_score": score,
        }
    )


def should_refresh_terminal():
    global _last_update_time
    return (time.time() - _last_update_time) >= 3


def render_terminal():
    global _last_update_time
    _last_update_time = time.time()

    ascii_banner = pyfiglet.figlet_format("QuietEye", font="slant")
    ascii_renderable = Text(ascii_banner, style="bold green")

    table = Table.grid(padding=1)
    table.add_column(justify="right", style="cyan", no_wrap=True)
    table.add_column(style="bold white")

    table.add_row("Frame", str(_frame_data["frame"]))
    table.add_row("Gaze Direction", _frame_data["gaze"])
    table.add_row("Head Pitch", f"{_frame_data['pitch']:.2f}")
    table.add_row("Head Yaw", f"{_frame_data['yaw']:.2f}")
    table.add_row("Head Status", _frame_data["head_status"])
    table.add_row("Attention Score", f"{_frame_data['attention_score']:.2f}")

    return Group(
        Align.center(ascii_renderable),
        Panel(table, title="Attention Metrics", border_style="bold blue"),
    )


def start_terminal_display():
    global stop_display
    stop_display = False
    with Live(render_terminal(), refresh_per_second=1, screen=True) as live:
        while not stop_display:
            if should_refresh_terminal():
                live.update(render_terminal())
            time.sleep(0.1)


def stop_terminal_display():
    global stop_display
    stop_display = True
