import os
import sys
import json
import shutil

AUTO_SAFE_DIRS = {
    "node_modules",
    "target",
    "build",
    "dist",
    "out",
    "__pycache__",
    ".pytest_cache",
    ".gradle",
    ".next",
    "coverage",
    ".cache",
    ".mypy_cache",
    ".ruff_cache"
}

AUTO_SAFE_FILES = {
    ".log",
    ".tmp",
    ".temp",
    ".bak",
    ".pyc",
    ".class"
}

def detect_project_type(root):
    if os.path.exists(os.path.join(root, "pom.xml")):
        return "Java Maven"

    if os.path.exists(os.path.join(root, "build.gradle")):
        return "Java Gradle"

    if os.path.exists(os.path.join(root, "package.json")):
        return "NodeJS"

    if os.path.exists(os.path.join(root, "requirements.txt")):
        return "Python"

    return "Unknown"

def get_folder_size(folder):
    total = 0

    for root, _, files in os.walk(folder):
        for file in files:
            try:
                total += os.path.getsize(
                    os.path.join(root, file)
                )
            except:
                pass

    return total

def collect_candidates(project_root):
    candidates = []
    visited = set()

    for current_root, dirs, files in os.walk(project_root):

        for d in dirs[:]:
            if d.lower() in AUTO_SAFE_DIRS:

                full_path = os.path.join(
                    current_root,
                    d
                )

                if full_path not in visited:
                    visited.add(full_path)

                    candidates.append({
                        "type": "directory",
                        "path": full_path,
                        "size_bytes": get_folder_size(
                            full_path
                        ),
                        "classification": "SAFE_TO_DELETE",
                        "reason": f"{d} is a generated/cache/build directory"
                    })

                dirs.remove(d)

        for file in files:

            ext = os.path.splitext(file)[1].lower()

            if ext in AUTO_SAFE_FILES:

                full_path = os.path.join(
                    current_root,
                    file
                )

                if full_path not in visited:

                    visited.add(full_path)

                    try:
                        size = os.path.getsize(
                            full_path
                        )
                    except:
                        size = 0

                    candidates.append({
                        "type": "file",
                        "path": full_path,
                        "size_bytes": size,
                        "classification": "SAFE_TO_DELETE",
                        "reason": f"{ext} temporary/generated file"
                    })

    return candidates

def bytes_to_mb(size):
    return round(size / (1024 * 1024), 2)

def analyze(project_root):

    if not os.path.isdir(project_root):
        print("Invalid project path")
        return

    project_type = detect_project_type(
        project_root
    )

    print(f"\nProject Type : {project_type}")
    print("Scanning project...\n")

    results = collect_candidates(
        project_root
    )

    total_size = sum(
        item["size_bytes"]
        for item in results
    )

    report = {
        "project_type": project_type,
        "total_candidates": len(results),
        "total_recoverable_mb": bytes_to_mb(
            total_size
        ),
        "items": results
    }

    report_file = os.path.join(
        project_root,
        "cleanup_report.json"
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

    print(
        f"Candidates Found : {len(results)}"
    )

    print(
        f"Recoverable Space : "
        f"{bytes_to_mb(total_size)} MB"
    )

    print(
        f"Report Created : {report_file}"
    )

def clean(project_root):

    report_file = os.path.join(
        project_root,
        "cleanup_report.json"
    )

    if not os.path.exists(report_file):
        print(
            "Run analyze first."
        )
        return

    with open(
        report_file,
        "r",
        encoding="utf-8"
    ) as f:
        report = json.load(f)

    deleted = 0
    freed = 0

    for item in report["items"]:

        path = item["path"]

        try:

            if item["type"] == "directory":
                shutil.rmtree(path)

            else:
                os.remove(path)

            deleted += 1
            freed += item["size_bytes"]

            print(
                f"Deleted: {path}"
            )

        except Exception as e:

            print(
                f"Failed: {path}"
            )

            print(e)

    print("\nCleanup Complete")

    print(
        f"Deleted Items : {deleted}"
    )

    print(
        f"Freed Space : "
        f"{bytes_to_mb(freed)} MB"
    )

def usage():
    print(
        "\nUsage:"
        "\npython ai_cleanup.py analyze <project>"
        "\npython ai_cleanup.py clean <project>\n"
    )

if __name__ == "__main__":

    if len(sys.argv) != 3:
        usage()
        sys.exit(1)

    command = sys.argv[1].lower()

    project_path = os.path.abspath(
        sys.argv[2]
    )

    if command == "analyze":
        analyze(project_path)

    elif command == "clean":
        clean(project_path)

    else:
        usage()