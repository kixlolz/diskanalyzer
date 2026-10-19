# diskanalyzer

Interactive disk usage analyzer with a TUI. Find what's eating your disk.

[![tests](https://github.com/kixlolz/diskanalyzer/actions/workflows/test.yml/badge.svg)](https://github.com/kixlolz/diskanalyzer/actions/workflows/test.yml)

## Quick start (Windows)

Double-click `start.bat`. It creates a venv, installs dependencies, and prompts for a directory to scan.

## Quick start (any OS)

```bash
python -m venv .venv
# Windows:  .\.venv\Scripts\Activate.ps1
# Unix:     source .venv/bin/activate
pip install -e .
diskanalyzer ~/Downloads
```

## Usage

```bash
diskanalyzer ~/Downloads              # TUI
diskanalyzer ~/Downloads --plain      # table (auto when piped)
diskanalyzer ~/Downloads --plain --top 20
```

## Features

- Recursive size computation, sorted by size
- Safe: skips symlinks, records permission errors per node
- TUI: interactive tree, drill into any folder
- `--plain` mode for scripts and CI (auto-detected when stdout isn't a TTY)

## Layout

```
diskanalyzer/
  scanner.py     # filesystem walk + size aggregation
  tui.py         # Textual app
  cli.py         # argparse entrypoint
```

## Tests

```bash
pip install pytest
pytest
```

## License

MIT