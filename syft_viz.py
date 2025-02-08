#!/usr/bin/env python3
import re
import sys
from rich.console import Console
from rich.table import Table
from rich import box
from dataclasses import dataclass
from typing import List
import math

@dataclass
class TaskTiming:
    name: str
    duration: float  # in seconds
    
def parse_duration(duration_str: str) -> float:
    """Convert duration string to seconds."""
    if 'ms' in duration_str:
        return float(duration_str.replace('ms', '')) / 1000
    elif 'µs' in duration_str:
        return float(duration_str.replace('µs', '')) / 1000000
    elif 's' in duration_str:
        return float(duration_str.replace('s', ''))
    return 0

def parse_syft_output(lines: List[str]) -> List[TaskTiming]:
    """Parse syft verbose output into task timings."""
    pattern = r'task completed elapsed=(\d+\.?\d*(?:ms|µs|s)) task=([^\s]+)'
    timings = []
    
    for line in lines:
        match = re.search(pattern, line)
        if match:
            duration_str, task_name = match.groups()
            duration = parse_duration(duration_str)
            timings.append(TaskTiming(task_name, duration))
    
    return timings

def create_bar_chart(timings: List[TaskTiming], width: int = 40) -> Table:
    """Create a rich table with bar chart visualization."""
    total_time = sum(t.duration for t in timings)
    sorted_timings = sorted(timings, key=lambda x: x.duration, reverse=True)
    
    table = Table(box=box.MINIMAL, show_header=False, width=100)
    table.add_column("Task", style="cyan")
    table.add_column("Time", style="green")
    table.add_column("Bar", style="blue")
    table.add_column("%", style="yellow")
    
    for timing in sorted_timings:
        percentage = (timing.duration / total_time) * 100
        if percentage < 0.01:  # Skip very small percentages
            continue
            
        bar_length = math.ceil((timing.duration / total_time) * width)
        bar = "█" * bar_length
        
        # Format duration string
        if timing.duration >= 1:
            duration_str = f"{timing.duration:.2f}s"
        elif timing.duration >= 0.001:
            duration_str = f"{timing.duration * 1000:.2f}ms"
        else:
            duration_str = f"{timing.duration * 1000000:.2f}µs"
            
        table.add_row(
            timing.name,
            duration_str,
            bar,
            f"{percentage:.1f}%"
        )
    
    return table

def main():
    # If no file is provided, read from stderr if it's being piped, otherwise stdin
    if len(sys.argv) == 1:
        if not sys.stdin.isatty():  # Check if input is being piped
            lines = sys.stdin.readlines()
        else:
            print("No input provided. Either pipe syft output or provide a file.", file=sys.stderr)
            sys.exit(1)
    else:
        # Read from file if provided
        try:
            with open(sys.argv[1]) as f:
                lines = f.readlines()
        except FileNotFoundError:
            print(f"File {sys.argv[1]} not found", file=sys.stderr)
            sys.exit(1)

    timings = parse_syft_output(lines)
    if not timings:
        print("No timing data found in input", file=sys.stderr)
        sys.exit(1)
        
    console = Console()
    table = create_bar_chart(timings)
    console.print(table)

if __name__ == "__main__":
    main()
