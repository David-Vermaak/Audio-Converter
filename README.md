# Bulk Audio Converter

A simple Python GUI app to bulk convert audio files between formats (mp3, wav, ogg, flac) with a progress bar and terminal output.

## Features
- Multi-select audio files for conversion
- Filter files by input type ("Convert from")
- Choose output format ("Convert to")
- Progress bar and terminal-like log
- Responsive UI

## Requirements
- **Python 3.11**
- **ffmpeg** (installed and in PATH)

## Setup

### 1. Install Python 3.11
Download and install Python 3.11 from the [official website](https://www.python.org/downloads/release/python-3110/).

### 2. Install ffmpeg (using Chocolatey)
If you don't have [Chocolatey](https://chocolatey.org/install), install it first. Then, open an **Administrator** command prompt and run:

```
choco install ffmpeg -y
```

This will install ffmpeg and add it to your PATH automatically.

### 3. Install Python dependencies
Open a terminal in the project folder and run:

```
pip install pydub
```

## Usage
1. Run the app:
   ```
   python "#Python audio converter.py"
   ```
2. Use the GUI to:
   - Select the input file type ("Convert from")
   - Select audio files
   - Choose output format ("Convert to")
   - Select output folder
   - Click **Convert**
3. Watch the progress bar and terminal log for results.

---

**Note:** If you add new formats, make sure ffmpeg supports them. 