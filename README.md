# Android Assets Generator

A Python tool with a Graphical User Interface (GUI) to automatically generate Android `drawable` assets for all standard densities (mdpi, hdpi, xhdpi, xxhdpi, xxxhdpi) from a single source image.

This tool is inspired by a PowerShell script but built with Python and Tkinter for cross-platform compatibility and ease of use.

## Features
- **Auto-Density Detection**: Intelligently detects the base density of the input image to ensure correct downscaling/upscaling.
- **Android-Safe Filenames**: Automatically cleans filenames to meet Android resource naming conventions (lowercase, no spaces/special chars, invalid start characters).
- **Batch Processing**: Select a directory to process all images within it at once.
- **Custom Output**: Choose where the generated `android` folders will be saved.
- **GUI**: Simple and easy-to-use interface.

## Prerequisites
- Python 3.x
- [Pillow](https://python-pillow.org/) library.

## Installation

1. Clone or download this repository.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python main.py
   ```
2. **Input Mode**: Choose between "Single Image File" or "Directory (Batch)".
3. **Select Input**: Click "Browse..." to select your file or folder.
4. **Output Directory**: (Optional) Select a specific output location. Defaults to an `android` folder in the same location as the input.
5. **Generate**: Click "Generate Assets".
6. Monitor the logs in the text area for progress and details about the generated files.

## Generated Structure
```
Output Directory/
└── android/
    ├── drawable-mdpi/
    │   └── image.png
    ├── drawable-hdpi/
    │   └── image.png
    ├── drawable-xhdpi/
    │   └── image.png
    ├── drawable-xxhdpi/
    │   └── image.png
    └── drawable-xxxhdpi/
    │   └── image.png
```
