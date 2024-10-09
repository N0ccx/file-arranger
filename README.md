# File Organizer Script

This Python script helps you organize files from specific directories (like Desktop, Downloads, Music, Pictures, and Videos) by sorting them based on file types and creation dates. It can also check for duplicate files and create a backup of the directory before making any changes.

## Features

- **Organize files by type** (e.g., images, music, documents).
- **Sort files by creation date** (e.g., sort into folders by month/year like `2024-10`).
- **Detect duplicate files** using file content (hashing).
- **Backup** your files before moving them.
- **Dry-run mode** to see what changes would be made without actually moving files.

## Requirements

Make sure you have [Python](https://www.python.org/downloads/) installed on your machine.

## Installation

1. Clone or download this repository.
   ```bash
   git clone https://github.com/n0ccx/file-arranger.git\
2. Navigate to the project directory.

bash

      cd file-arranger
3.Ensure Python is installed. You can check by running:

bash

    python --version

## Usage
# Run the Script

You can run the script from your terminal (Mac/Linux) or command prompt (Windows).
# Basic Commands

   Organize default folders (Desktop, Downloads, etc.) with a backup:

   bash

      python file_arranger.py --backup

This will sort files in your default folders (Desktop, Downloads, Music, Pictures, Videos) and create a backup in a .zip file before making changes.

Perform a dry-run (test what would happen without moving files):

bash

      python file_arranger.py --dir /path/to/folder --dry-run

This command will show you what changes would be made without actually moving any files.

Organize files from a specific folder:

bash

      python file_arranger.py --dir /path/to/folder

Replace /path/to/folder with the path to the folder you want to organize. This will move files based on their type (e.g., images, music, documents).

Organize only specific file types (e.g., .mp3, .jpg):

bash

    python file_arranger.py --dir /path/to/folder --types mp3 jpg

   This command will only organize .mp3 and .jpg files.

## Options
# Command	Description
--dir	Specify a custom directory to scan. Default: Desktop, Downloads, Music, Pictures, Videos.
--types	Only organize certain file types (e.g., mp3, jpg, txt).
--backup	Create a backup of the directory before organizing the files.
--dry-run	Perform a dry-run without actually moving files (simulates the organization process).
# Example Commands

   Organize default directories with a backup:

   bash

      python file_arranger.py --backup

Organize files in a specific folder and perform a dry run:

bash

      python file_arranger.py --dir /Users/John/Documents --dry-run

Sort only .jpg and .mp3 files in your Downloads folder:

bash

      python file_arranger.py --dir /Users/John/Downloads --types jpg mp3

Organize files in the Pictures folder without creating a backup:

bash

    python file_arranger.py --dir /Users/John/Pictures

## How It Works

   Sorting by File Type: The script will look at each file's extension (e.g., .jpg, .mp3) and move it to a corresponding folder like Images, Music, Documents, etc.

   Organizing by Date: Inside the folder (like Images), files are further organized into subfolders by the month and year they were created (e.g., 2024-10 for files created in October 2024).

   Duplicate Detection: The script calculates a unique fingerprint (hash) for each file. If it finds two files with the same fingerprint, it considers them duplicates and skips moving the duplicate.

   Backup: If the --backup option is used, the script creates a .zip file containing all the files in the folder before it starts organizing them. This ensures that you can restore your files if something goes wrong.

   Dry-Run Mode: If you use the --dry-run option, the script will only simulate what would happen without moving any files. This is useful for checking before making any changes.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
## Contributing

If you'd like to contribute to this project, feel free to fork the repo and submit a pull request!


