
import os
import shutil
import logging
from pathlib import Path

# ==========================================
# AUTOMATED FILE ORGANIZER AND CLEANUP UTILITY
# ==========================================

# Project directory
BASE_DIR = Path(__file__).resolve().parent

# Logging directory
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Configure logging
logging.basicConfig(
    filename=LOG_DIR / "organizer.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# File extension mapping
EXTENSION_MAPPING = {
    # Documents
    ".pdf": "Documents",
    ".doc": "Documents",
    ".docx": "Documents",
    ".txt": "Documents",
    ".xls": "Documents",
    ".xlsx": "Documents",
    ".ppt": "Documents",
    ".pptx": "Documents",

    # Images
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".gif": "Images",
    ".bmp": "Images",
    ".webp": "Images",

    # Videos
    ".mp4": "Videos",
    ".mkv": "Videos",
    ".avi": "Videos",
    ".mov": "Videos",

    # Archives
    ".zip": "Archives",
    ".rar": "Archives",
    ".7z": "Archives",
    ".tar": "Archives",
    ".gz": "Archives",

    # Code files
    ".py": "Code",
    ".java": "Code",
    ".cpp": "Code",
    ".c": "Code",
    ".html": "Code",
    ".css": "Code",
    ".js": "Code",
    ".php": "Code"
}

# Temporary file extensions
TEMP_EXTENSIONS = {
    ".tmp", ".temp", ".bak", ".old", ".cache"
}


# ==========================================
# FUNCTION 1: GENERATE UNIQUE FILE NAME
# ==========================================

def get_unique_path(destination):

    if not destination.exists():
        return destination

    folder = destination.parent
    name = destination.stem
    extension = destination.suffix
    counter = 1

    while True:

        new_path = folder / f"{name}_{counter}{extension}"

        if not new_path.exists():
            return new_path

        counter += 1


# ==========================================
# FUNCTION 2: ORGANIZE FILES
# ==========================================

def organize_files(folder):

    moved = 0
    failed = 0
    skipped = 0

    try:

        with os.scandir(folder) as entries:

            for entry in entries:

                if not entry.is_file(follow_symlinks=False):
                    continue

                source = Path(entry.path)

                # Avoid moving this program's own files
                if source.resolve() == Path(__file__).resolve():
                    continue

                if LOG_DIR in source.parents:
                    continue

                # Find category
                category = EXTENSION_MAPPING.get(
                    source.suffix.lower(),
                    "Others"
                )

                destination_folder = folder / category

                try:

                    # Create category folder
                    destination_folder.mkdir(
                        parents=True,
                        exist_ok=True
                    )

                    # Generate safe destination name
                    destination = get_unique_path(
                        destination_folder / source.name
                    )

                    # Move file
                    shutil.move(
                        str(source),
                        str(destination)
                    )

                    print(
                        f"[MOVED] {source.name} -> {category}"
                    )

                    logging.info(
                        f"Moved {source.name} to {category}"
                    )

                    moved += 1

                except PermissionError:

                    print(f"[ERROR] Permission denied: {source.name}")
                    logging.error(
                        f"Permission denied: {source.name}"
                    )
                    failed += 1

                except FileExistsError:

                    print(f"[ERROR] File already exists: {source.name}")
                    logging.error(
                        f"File already exists: {source.name}"
                    )
                    failed += 1

                except OSError as error:

                    print(f"[ERROR] Cannot move {source.name}: {error}")
                    logging.error(
                        f"Cannot move {source.name}: {error}"
                    )
                    failed += 1

    except PermissionError:

        print("[ERROR] Cannot access selected folder.")
        logging.error("Permission denied while scanning folder.")
        failed += 1

    return moved, skipped, failed


# ==========================================
# FUNCTION 3: CLEAN TEMPORARY FILES
# ==========================================

def cleanup_files(folder):

    deleted = 0
    failed = 0
    skipped = 0

    print("\n===== TEMPORARY FILE CLEANUP =====")

    try:

        with os.scandir(folder) as entries:

            for entry in entries:

                if not entry.is_file(follow_symlinks=False):
                    continue

                source = Path(entry.path)

                if source.suffix.lower() not in TEMP_EXTENSIONS:
                    continue

                confirmation = input(
                    f"Delete {source.name}? (yes/no): "
                ).strip().lower()

                if confirmation != "yes":

                    skipped += 1
                    print(f"[SKIPPED] {source.name}")
                    continue

                try:

                    source.unlink()

                    print(f"[DELETED] {source.name}")

                    logging.info(
                        f"Deleted temporary file: {source.name}"
                    )

                    deleted += 1

                except PermissionError:

                    print(f"[ERROR] Permission denied: {source.name}")
                    logging.error(
                        f"Permission denied: {source.name}"
                    )
                    failed += 1

                except OSError as error:

                    print(f"[ERROR] Cannot delete {source.name}: {error}")
                    logging.error(
                        f"Cannot delete {source.name}: {error}"
                    )
                    failed += 1

    except PermissionError:

        print("[ERROR] Cannot access folder.")
        failed += 1

    return deleted, skipped, failed


# ==========================================
# FUNCTION 4: REMOVE EMPTY FOLDERS
# ==========================================

def remove_empty_folders(folder):

    removed = 0
    failed = 0

    # Scan folders from deepest to topmost
    for current, directories, files in os.walk(
        folder,
        topdown=False
    ):

        current_path = Path(current)

        # Never remove the selected main folder
        if current_path == folder:
            continue

        try:

            # Remove only empty folders
            if not any(current_path.iterdir()):

                current_path.rmdir()

                print(
                    f"[REMOVED EMPTY FOLDER] {current_path.name}"
                )

                logging.info(
                    f"Removed empty folder: {current_path}"
                )

                removed += 1

        except PermissionError:

            print(
                f"[ERROR] Permission denied: {current_path.name}"
            )
            failed += 1

        except OSError as error:

            logging.error(
                f"Could not remove folder {current_path}: {error}"
            )
            failed += 1

    return removed, failed


# ==========================================
# FUNCTION 5: EXECUTION SUMMARY
# ==========================================

def show_summary(moved, deleted, removed, skipped, failed):

    print("\n")
    print("=" * 45)
    print(" AUTOMATED FILE ORGANIZER AND CLEANUP UTILITY")
    print("=" * 45)

    print(f"Files organized          : {moved}")
    print(f"Temporary files deleted  : {deleted}")
    print(f"Empty folders removed    : {removed}")
    print(f"Operations skipped       : {skipped}")
    print(f"Failed operations        : {failed}")

    print("=" * 45)
    print("Execution completed!")

    print(f"Log saved at: {LOG_DIR / 'organizer.log'}")


# ==========================================
# MAIN FUNCTION
# ==========================================

def main():

    print("\n")
    print("=" * 50)
    print(" AUTOMATED FILE ORGANIZER AND CLEANUP UTILITY")
    print("=" * 50)

    folder_input = input(
        "\nEnter folder path to organize: "
    ).strip().strip('"')

    folder = Path(folder_input).expanduser()

    # Validate folder
    if not folder.exists():

        print("[ERROR] Folder does not exist.")
        return

    if not folder.is_dir():

        print("[ERROR] Provided path is not a folder.")
        return

    print("\nSelect an operation:")
    print("1. Organize Files")
    print("2. Cleanup Temporary Files")
    print("3. Remove Empty Folders")
    print("4. Run All Operations")
    
    choice = input(
        "\nEnter your choice (1-4): "
    ).strip()

    moved = 0
    deleted = 0
    removed = 0
    skipped = 0
    failed = 0

    # Organize files
    if choice == "1" or choice == "4":

        print("\n===== FILE ORGANIZATION =====")

        moved, skip_count, error_count = organize_files(folder)

        skipped += skip_count
        failed += error_count

    # Cleanup temporary files
    if choice == "2" or choice == "4":

        deleted, skip_count, error_count = cleanup_files(folder)

        skipped += skip_count
        failed += error_count

    # Remove empty folders
    if choice == "3" or choice == "4":

        print("\n===== EMPTY FOLDER CLEANUP =====")

        removed, error_count = remove_empty_folders(folder)

        failed += error_count

    # Invalid selection
    if choice not in ("1", "2", "3", "4"):

        print("[ERROR] Invalid choice. Select 1, 2, 3 or 4.")
        return

    # Display final summary
    show_summary(
        moved,
        deleted,
        removed,
        skipped,
        failed
    )


# ==========================================
# PROGRAM ENTRY POINT
# ==========================================

if __name__ == "__main__":
    main()
