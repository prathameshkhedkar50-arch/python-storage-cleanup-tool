import os
import sys
from collections import defaultdict

JUNK_EXTENSIONS = {
    ".tmp",".temp",".bak",".old",".log",".cache",".dmp",
    ".class",".obj",".o",".pdb",".ilk",".pyc"
}

def format_size(size):
    for unit in ["B","KB","MB","GB","TB"]:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"

def scan(drive):
    folder_sizes = defaultdict(int)
    junk_count = 0
    junk_size = 0
    total_files = 0

    print(f"Scanning {drive} ...\n")

    for root, dirs, files in os.walk(drive):
        for file in files:
            try:
                path = os.path.join(root, file)
                size = os.path.getsize(path)

                total_files += 1
                folder_sizes[root] += size

                ext = os.path.splitext(file)[1].lower()

                if ext in JUNK_EXTENSIONS:
                    junk_count += 1
                    junk_size += size

            except:
                pass

    print(f"Total Files : {total_files}")
    print(f"Junk Files  : {junk_count}")
    print(f"Junk Size   : {format_size(junk_size)}")

    print("\nTop 20 Largest Folders")
    print("-" * 80)

    top_folders = sorted(
        folder_sizes.items(),
        key=lambda x: x[1],
        reverse=True
    )[:20]

    for folder, size in top_folders:
        print(f"{format_size(size):>12}  {folder}")

if len(sys.argv) != 3 or sys.argv[1].lower() != "scan":
    print("Usage: python trash.py scan D:/")
    sys.exit(1)

scan(sys.argv[2])