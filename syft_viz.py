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
    if not duration_str:
        return 0

    try:
        # Handle minutes format (e.g., "20m47.611789051s")
        if 'm' in duration_str and 's' in duration_str and not 'ms' in duration_str:
            minutes_part = duration_str.split('m')[0]
            seconds_part = duration_str.split('m')[1].rstrip('s')
            
            minutes = float(minutes_part)
            seconds = float(seconds_part) if seconds_part else 0
            return minutes * 60 + seconds
            
        # Handle milliseconds
        elif 'ms' in duration_str:
            return float(duration_str.replace('ms', '')) / 1000
            
        # Handle microseconds
        elif 'µs' in duration_str:
            return float(duration_str.replace('µs', '')) / 1000000
            
        # Handle plain seconds
        elif 's' in duration_str:
            return float(duration_str.replace('s', ''))
            
        return 0
    except (ValueError, IndexError) as e:
        print(f"Warning: Could not parse duration: {duration_str} - {str(e)}", file=sys.stderr)
        return 0

def parse_syft_output(lines: List[str]) -> List[TaskTiming]:
    """Parse syft verbose output into task timings."""
    # Two patterns: one for direct syft output, one for library usage
    patterns = [
        r'task completed elapsed=([0-9]+\.?[0-9]*(?:m)?(?:[0-9]+\.?[0-9]*)?(?:ms|µs|s)) (?:from-lib=syft )?task=([^\s]+)',
    ]
    timings = []
    
    for line in lines:
        for pattern in patterns:
            match = re.search(pattern, line)
            if match:
                duration_str, task_name = match.groups()
                try:
                    duration = parse_duration(duration_str)
                    timings.append(TaskTiming(task_name, duration))
                except ValueError as e:
                    print(f"Warning: Error parsing line: {line.strip()}", file=sys.stderr)
                break
    
    return timings

def format_duration(seconds: float) -> str:
    """Format duration in a human readable way."""
    if seconds >= 60:
        minutes = int(seconds // 60)
        remaining_seconds = seconds % 60
        return f"{minutes}m{remaining_seconds:.2f}s"
    elif seconds >= 1:
        return f"{seconds:.2f}s"
    elif seconds >= 0.001:
        return f"{seconds * 1000:.2f}ms"
    else:
        return f"{seconds * 1000000:.2f}µs"
    
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
            
        table.add_row(
            timing.name,
            format_duration(timing.duration),
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
