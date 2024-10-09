import os
import shutil
from datetime import datetime
import argparse  # This helps us add options to the script
import hashlib   # This helps us check if two files are exactly the same (duplicates)
import zipfile   # This helps us create a zip backup of files
import logging   # This helps us keep track of what the script is doing

# Set up logging to write everything the script does to a file
logging.basicConfig(filename='file_organizer.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# These are the folders we want to organize (default directories)
default_directories = [
    os.path.join(os.path.expanduser("~"), "Desktop"),
    os.path.join(os.path.expanduser("~"), "Downloads"),
    os.path.join(os.path.expanduser("~"), "Music"),
    os.path.join(os.path.expanduser("~"), "Pictures"),
    os.path.join(os.path.expanduser("~"), "Videos"),
]

# These are the types of files and where we want to move them (organized by extension)
folders = {
    'txt': 'Documents',
    'pdf': 'Documents',
    'docx': 'Documents',
    'jpeg': 'Images',
    'jpg': 'Images',
    'png': 'Images',
    'mp3': 'Music',
    'wav': 'Music',
    'mp4': 'Videos',
    'mov': 'Videos',
    'zip': 'Archives',
    'rar': 'Archives',
    'py': 'Code',
    'exe': 'Programs'
}

# We'll use this dictionary to remember which files we've seen already (for duplicates)
file_hashes = {}

# This function reads any options we give the script (like which folder to organize)
def parse_arguments():
    parser = argparse.ArgumentParser(description="Organize files by extension, date, and detect duplicates.")
    parser.add_argument("--dir", type=str, help="Specify a directory to scan (default: standard directories)", default=None)
    parser.add_argument("--types", nargs='+', help="Specify file types to organize (e.g., txt mp3 jpg)", default=None)
    parser.add_argument("--backup", action='store_true', help="Create a backup before organizing files.")
    parser.add_argument("--dry-run", action='store_true', help="Perform a dry run without moving files.")
    return parser.parse_args()

# This is a helper function to print messages to the screen and also save them in the log file
def log_action(message):
    print(message)
    logging.info(message)

# This function creates a folder if it doesn't exist already
def create_directory_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

# This function organizes files by their creation date (puts them in folders like "2024-10")
def organize_files_by_date(file_path, destination_folder):
    creation_time = os.path.getctime(file_path)
    date_folder = datetime.fromtimestamp(creation_time).strftime('%Y-%m')
    dated_folder = os.path.join(destination_folder, date_folder)
    create_directory_if_not_exists(dated_folder)
    return dated_folder

# This function creates a unique code (called a hash) for each file, which helps us check for duplicates
def calculate_file_hash(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# This checks if a file is a duplicate of another file we’ve already seen
def check_duplicates(file_path):
    file_hash = calculate_file_hash(file_path)
    if file_hash in file_hashes:
        return True, file_hashes[file_hash]
    else:
        file_hashes[file_hash] = file_path
        return False, None

# This function moves the file or just tells you where it would move the file (if dry-run is enabled)
def move_file(file_path, destination_path, dry_run=False):
    if dry_run:
        log_action(f"DRY RUN: Would move '{file_path}' to '{destination_path}'")
    else:
        shutil.move(file_path, destination_path)
        log_action(f"Moved '{file_path}' to '{destination_path}'")

# This function creates a backup (zip) of all files in the directory before moving them
def create_backup(directory):
    backup_dir = os.path.join(directory, 'Backup')
    backup_path = os.path.join(backup_dir, 'backup.zip')
    create_directory_if_not_exists(backup_dir)

    with zipfile.ZipFile(backup_path, 'w') as backup_zip:
        for foldername, subfolders, filenames in os.walk(directory):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                backup_zip.write(file_path, os.path.relpath(file_path, directory))

    log_action(f"Backup created at {backup_path}")

# This function sorts files by type (like music or images) and checks for duplicates
def sort_files(directory, file_types=None, dry_run=False):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        # Only move files, skip folders
        if os.path.isfile(file_path):
            ext = filename.split('.')[-1].lower()

            # If the user only wants to sort certain types of files, we skip others
            if file_types and ext not in file_types:
                continue

            # Find out where to move the file (based on its type)
            destination_folder = folders.get(ext, 'Others')  # Default to 'Others' if we don't know the type
            destination_folder_path = os.path.join(directory, destination_folder)

            # Create the destination folder if it doesn't exist
            create_directory_if_not_exists(destination_folder_path)

            # Organize files into date folders (like "2024-10")
            final_destination = organize_files_by_date(file_path, destination_folder_path)
            destination_path = os.path.join(final_destination, filename)

            # Check if the file is a duplicate
            is_duplicate, duplicate_path = check_duplicates(file_path)
            if is_duplicate:
                log_action(f"Duplicate file detected: '{filename}' already exists as '{duplicate_path}'")
                continue

            # If a file with the same name exists, we add a number (so we don't overwrite it)
            if os.path.exists(destination_path):
                name, ext = os.path.splitext(filename)
                counter = 1
                while os.path.exists(destination_path):
                    destination_path = os.path.join(final_destination, f"{name}_{counter}{ext}")
                    counter += 1

            # Move the file (or simulate it if dry-run is enabled)
            move_file(file_path, destination_path, dry_run)

# This scans the given folders, and optionally creates a backup and checks for duplicates
def scan_and_sort_directories(directories, file_types=None, backup=False, dry_run=False):
    for directory in directories:
        if os.path.exists(directory):
            log_action(f"Scanning directory: {directory}")

            # Create a backup if requested
            if backup and not dry_run:
                create_backup(directory)

            sort_files(directory, file_types, dry_run)
        else:
            log_action(f"Directory not found: {directory}")

if __name__ == "__main__":
    # Get the user’s input from the command line (if any)
    args = parse_arguments()

    # If the user gave us a folder to scan, use that, otherwise use the default folders
    directories_to_scan = [args.dir] if args.dir else default_directories

    # Organize files with backup or dry-run mode
    scan_and_sort_directories(directories_to_scan, file_types=args.types, backup=args.backup, dry_run=args.dry_run)
