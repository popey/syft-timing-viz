# Syft Timing Visualizer

A simple Python script to visualize the timing data from Syft's verbose output. 

When running Syft with the `-v` flag to generate SBOMs, it outputs timing information for each cataloger. This tool creates an easy-to-read terminal visualization showing the proportion of time spent in each stage.

## Features

- Creates a proportional bar chart of time spent in each Syft cataloger
- Sorts tasks by duration
- Displays timing in appropriate units (seconds, milliseconds, microseconds)
- Shows percentage of total time for each task
- Filters out very small percentages to keep output clean
- Supports both piped input and file reading

## Requirements

- Python 3.7+
- [rich](https://github.com/Textualize/rich) library

## Installation

First, clone this repository:
```bash
git clone https://github.com/popey/syft-timing-viz
cd syft-timing-viz
```

Then choose your preferred Python environment setup:

### Using venv (Python's built-in virtual environment)
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate

# Install dependencies
pip install rich
```

### Using uv
```bash
# Create and activate virtual environment
uv venv
source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate

# Install dependencies
uv pip install rich
```

### Global installation (not recommended)
```bash
pip install rich
```

Finally, make the scripts executable:
```bash
chmod +x syft_viz.py
chmod +x syft-viz
```

## Usage

You can use the script in several ways:

1. Using the wrapper script (recommended):
```bash
./syft-viz ubuntu:latest
```

2. Pipe Syft output directly (note the 2>&1 to capture verbose output):
```bash
syft -v ubuntu:latest 2>&1 | ./syft_viz.py
```

3. Save Syft output to a file and provide it as an argument:
```bash
syft -v ubuntu:latest > syft_output.txt 2>&1
./syft_viz.py syft_output.txt
```

Note: The `2>&1` is required because Syft sends its verbose output to stderr rather than stdout.

## Example Output

```
  file-digest-cataloger              │ 263.36ms    │ █████████████████████        │ 51.6%
  dpkg-db-cataloger                  │ 67.86ms     │ ██████                       │ 13.3%
  file-executable-cataloger          │ 37.62ms     │ ███                          │ 7.4%
  relationships-cataloger            │ 32.88ms     │ ███                          │ 6.4%
  go-module-binary-cataloger         │ 20.52ms     │ ██                           │ 4.0%
  graalvm-native-image-cataloger     │ 20.37ms     │ ██                           │ 4.0%
  cargo-auditable-binary-cataloger   │ 20.09ms     │ ██                           │ 3.9%
  elf-binary-package-cataloger       │ 17.09ms     │ ██                           │ 3.3%
  unknowns-labeler                   │ 10.00ms     │ █                            │ 2.0%
  file-metadata-cataloger            │ 9.36ms      │ █                            │ 1.8%
  binary-classifier-cataloger        │ 6.57ms      │ █                            │ 1.3%
  nix-store-cataloger                │ 1.91ms      │ █                            │ 0.4%
  linux-kernel-cataloger             │ 929.62µs    │ █                            │ 0.2%
  environment-cataloger              │ 853.71µs    │ █                            │ 0.2%
  portage-cataloger                  │ 88.83µs     │ █                            │ 0.0%
  alpm-db-cataloger                  │ 76.92µs     │ █                            │ 0.0%
  java-archive-cataloger             │ 70.75µs     │ █                            │ 0.0%
  lua-rock-cataloger                 │ 68.92µs     │ █                            │ 0.0%
  php-pecl-serialized-cataloger      │ 61.38µs     │ █                            │ 0.0%
```

## Files

- `syft_viz.py`: The main Python script that processes and visualizes the timing data
- `syft-viz`: A convenience wrapper script that handles stderr redirection automatically
- `requirements.txt`: Python package dependencies

## Contributing

Pull requests are welcome! Please feel free to submit issues and enhancement requests.

## License

[MIT](LICENSE)

## Acknowledgments

- [Syft](https://github.com/anchore/syft) - The SBOM tool this visualizer is designed for
- [rich](https://github.com/Textualize/rich) - For beautiful terminal formatting
