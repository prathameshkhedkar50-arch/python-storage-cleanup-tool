import os
import sys
import json
import time
import hashlib
from collections import defaultdict

TEMP_EXTENSIONS = {
    ".tmp",".temp",".bak",".old",".log",".cache",
    ".dmp",".pyc",".class",".obj",".o",".ilk",".pdb"
}

CACHE_DIRS = {
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".cache",
    ".gradle",
    ".next",
    "coverage",
    "target",
    "build",
    "dist",
    "out"
}

RECYCLE_NAMES = {
    "$recycle.bin",
    "recycler",
    ".trash",
    ".trash-1000"
}

OLD_FILE_DAYS = 365
LARGE_FOLDER_MB = 500

def format_size(size):
    units = ["B","KB","MB","GB","TB"]
    for unit in units:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"

def get_folder_size(folder):
    total = 0

    try:
        for root, _, files in os.walk(folder):
            for file in files:
                try:
                    total += os.path.getsize(
                        os.path.join(root, file)
                    )
                except:
                    pass
    except:
        pass

    return total

def sha256_file(path):
    h = hashlib.sha256()

    try:
        with open(path, "rb") as f:
            while True:
                chunk = f.read(1024 * 1024)

                if not chunk:
                    break

                h.update(chunk)

        return h.hexdigest()

    except:
        return None
    
def is_excluded(path, excluded_path):

    if not excluded_path:
        return False

    path = os.path.abspath(path)
    excluded_path = os.path.abspath(excluded_path)

    return (
        path == excluded_path
        or path.startswith(
            excluded_path + os.sep
        )
    )

def scan(root_path, excluded_path=None):

    report = {
        "scan_time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "root": root_path,
        "excluded_path": excluded_path,
        "empty_folders": [],
        "empty_files": [],
        "temp_files": [],
        "cache_folders": [],
        "venv_folders": [],
        "node_modules": [],
        "maven_target": [],
        "pycache": [],
        "large_folders": [],
        "old_files": [],
        "recycle_like": [],
        "duplicates": []
    }

    total_files = 0
    total_size = 0

    folder_sizes = defaultdict(int)
    size_groups = defaultdict(list)

    old_threshold = (
        time.time() -
        (OLD_FILE_DAYS * 86400)
    )

    print(f"\nScanning: {root_path}")

    if excluded_path:
        print(
            f"Excluding: {excluded_path}"
        )

    print()

    for root, dirs, files in os.walk(root_path):

        dirs[:] = [
            d
            for d in dirs
            if not is_excluded(
                os.path.join(root, d),
                excluded_path
            )
        ]

        if is_excluded(
            root,
            excluded_path
        ):
            continue

        # KEEP ALL YOUR EXISTING
        # SCAN LOGIC BELOW THIS LINE

def scan(root_path):

    report = {
        "scan_time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "root": root_path,
        "empty_folders": [],
        "empty_files": [],
        "temp_files": [],
        "cache_folders": [],
        "venv_folders": [],
        "node_modules": [],
        "maven_target": [],
        "pycache": [],
        "large_folders": [],
        "old_files": [],
        "recycle_like": [],
        "duplicates": []
    }

    total_files = 0
    total_size = 0

    folder_sizes = defaultdict(int)
    size_groups = defaultdict(list)

    old_threshold = (
        time.time() -
        (OLD_FILE_DAYS * 86400)
    )

    print(f"\nScanning: {root_path}\n")

    for root, dirs, files in os.walk(root_path):

        if not files and not dirs:
            report["empty_folders"].append(root)

        for d in dirs:

            full_dir = os.path.join(
                root,
                d
            )

            name = d.lower()

            if name in CACHE_DIRS:

                size = get_folder_size(
                    full_dir
                )

                report["cache_folders"].append({
                    "path": full_dir,
                    "size": size
                })

                if name == "node_modules":
                    report["node_modules"].append({
                        "path": full_dir,
                        "size": size
                    })

                if name == "target":
                    report["maven_target"].append({
                        "path": full_dir,
                        "size": size
                    })

                if name == "__pycache__":
                    report["pycache"].append({
                        "path": full_dir,
                        "size": size
                    })

            if name == "venv":
                report["venv_folders"].append(
                    full_dir
                )

            if name in RECYCLE_NAMES:
                report["recycle_like"].append(
                    full_dir
                )

        for file in files:

            path = os.path.join(
                root,
                file
            )

            try:

                size = os.path.getsize(path)

                total_files += 1
                total_size += size

                folder_sizes[root] += size

                if size == 0:
                    report["empty_files"].append(
                        path
                    )

                ext = os.path.splitext(
                    file
                )[1].lower()

                if ext in TEMP_EXTENSIONS:
                    report["temp_files"].append({
                        "path": path,
                        "size": size
                    })

                modified = os.path.getmtime(
                    path
                )

                if modified < old_threshold:
                    report["old_files"].append({
                        "path": path,
                        "size": size,
                        "last_modified":
                        time.strftime(
                            "%Y-%m-%d",
                            time.localtime(
                                modified
                            )
                        )
                    })

                if size > 0:
                    size_groups[size].append(
                        path
                    )

            except:
                pass

    print("Checking large folders...")

    for folder, size in folder_sizes.items():

        if size >= (
            LARGE_FOLDER_MB *
            1024 *
            1024
        ):
            report["large_folders"].append({
                "path": folder,
                "size": size
            })

    print("Checking duplicates...")

    for size, files in size_groups.items():

        if len(files) < 2:
            continue

        hashes = defaultdict(list)

        for file in files:

            file_hash = sha256_file(
                file
            )

            if file_hash:
                hashes[file_hash].append(
                    file
                )

        for _, dups in hashes.items():

            if len(dups) > 1:

                report["duplicates"].append({
                    "size": size,
                    "files": dups
                })

    summary = {
        "total_files": total_files,
        "total_size": total_size,
        "empty_folders":
            len(report["empty_folders"]),
        "empty_files":
            len(report["empty_files"]),
        "temp_files":
            len(report["temp_files"]),
        "cache_folders":
            len(report["cache_folders"]),
        "venv_folders":
            len(report["venv_folders"]),
        "large_folders":
            len(report["large_folders"]),
        "old_files":
            len(report["old_files"]),
        "duplicate_groups":
            len(report["duplicates"])
    }

    report["summary"] = summary

    report_file = os.path.join(
        os.getcwd(),
        "trash_report.json"
    )

    with open(
        report_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            report,
            f,
            indent=4,
            ensure_ascii=False
        )

    print("\nSCAN COMPLETE")
    print("=" * 60)

    print(
        f"Total Files       : {total_files}"
    )

    print(
        f"Total Size        : "
        f"{format_size(total_size)}"
    )

    print(
        f"Empty Folders     : "
        f"{summary['empty_folders']}"
    )

    print(
        f"Empty Files       : "
        f"{summary['empty_files']}"
    )

    print(
        f"Temp Files        : "
        f"{summary['temp_files']}"
    )

    print(
        f"Cache Folders     : "
        f"{summary['cache_folders']}"
    )

    print(
        f"Virtual Envs      : "
        f"{summary['venv_folders']}"
    )

    print(
        f"Large Folders     : "
        f"{summary['large_folders']}"
    )

    print(
        f"Old Files         : "
        f"{summary['old_files']}"
    )

    print(
        f"Duplicate Groups  : "
        f"{summary['duplicate_groups']}"
    )

    print(
        f"\nReport Saved: "
        f"{report_file}"
    )
    


if __name__ == "__main__":

    if (
        len(sys.argv) < 3
        or sys.argv[1].lower() != "scan"
    ):
        print(
            "\nUsage:"
            "\npython drive_cleanup.py scan <path>"
            "\npython drive_cleanup.py scan <path> <exclude_path>\n"
        )
        sys.exit(1)

    root_path = os.path.abspath(
        sys.argv[2]
    )

    excluded_path = None

    if len(sys.argv) >= 4:
        excluded_path = os.path.abspath(
            sys.argv[3]
        )

    scan(
        root_path,
        excluded_path
    )