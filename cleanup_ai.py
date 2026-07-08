import os
import sys
import json
from groq import Groq


client = Groq(
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
)

def read_file(file_path):
    try:
        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:
            return f.read()
    except:
        return ""

def get_python_files(project_path):
    python_files = []

    for root, _, files in os.walk(project_path):

        for file in files:

            if file.endswith(".py"):

                python_files.append(
                    os.path.join(
                        root,
                        file
                    )
                )

    return python_files

def analyze_file(file_path, content):

    prompt = f"""
Analyze this Python file.

Determine if this file appears unused,
temporary, duplicate, test-only, old,
or not referenced by other code.

Return only JSON.

{{
  "unused": true,
  "confidence": 90,
  "reason": "reason"
}}

File:
{file_path}

Code:
{content[:12000]}
"""

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        result = response.choices[0].message.content.strip()

        start = result.find("{")
        end = result.rfind("}") + 1

        return json.loads(
            result[start:end]
        )

    except Exception as e:

        return {
            "unused": False,
            "confidence": 0,
            "reason": str(e)
        }

def clean_project(project_path):

    if not os.path.exists(project_path):

        print(
            f"Folder not found: {project_path}"
        )

        return

    python_files = get_python_files(
        project_path
    )

    print(
        f"\nFound {len(python_files)} Python files\n"
    )

    report = []

    for file_path in python_files:

        print(
            f"Checking: {file_path}"
        )

        content = read_file(
            file_path
        )

        if not content:
            continue

        result = analyze_file(
            file_path,
            content
        )

        item = {
            "file": file_path,
            "unused": result.get(
                "unused",
                False
            ),
            "confidence": result.get(
                "confidence",
                0
            ),
            "reason": result.get(
                "reason",
                ""
            )
        }

        report.append(
            item
        )

    with open(
        "cleanup_report.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            report,
            f,
            indent=4
        )

    print(
        "\nPotential Unused Files\n"
    )

    for item in report:

        if (
            item["unused"]
            and item["confidence"] >= 80
        ):

            print(
                f"{item['file']}"
            )

            print(
                f"Confidence : {item['confidence']}%"
            )

            print(
                f"Reason     : {item['reason']}\n"
            )

    print(
        "Report saved: cleanup_report.json"
    )

def main():

    if len(sys.argv) != 3:

        print(
            'Usage: python cleanup_ai.py clean "folder_path"'
        )

        return

    command = sys.argv[1].lower()

    folder_path = sys.argv[2]

    if command == "clean":

        clean_project(
            folder_path
        )

    else:

        print(
            f"Unknown command: {command}"
        )

if __name__ == "__main__":
    main()